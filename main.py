import os
import json
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Fridge AI Agent")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL_NAME = "llama-3.3-70b-versatile"

class RecipeRequest(BaseModel):
    ingredients: str

class FeedbackRequest(BaseModel):
    recipe_name: str
    rating: int # 1 for up, -1 for down
    comment: Optional[str] = None

class RecipeResponse(BaseModel):
    is_possible: bool
    recipes: List[dict] = [] # Added default empty list to prevent validation errors

@app.post("/generate-recipe", response_model=RecipeResponse)
async def generate_recipe(request: RecipeRequest):
    ingredients_str = request.ingredients.strip()
    
    if not ingredients_str:
        raise HTTPException(status_code=400, detail="Please enter some ingredients.")

    system_instruction = (
        "You are an elite, highly-trained professional chef AI. Your mission is to create recipes that are not only strict but also *delicious* and *culinary-logical*. "
        "Strict Rule: Use *only* the ingredients provided. Do NOT add salt, pepper, oil, water, or anything else unless listed. "
        "Culinary Rule: You must ensure the combination actually makes sense. Do NOT suggest disgusting or nonsensical combinations (like 'Cake and Tomato'). "
        "Logic: If the ingredients provided are fundamentally incompatible, return `is_possible: false`. "
        "Goal: Provide 1-3 distinct, high-quality recipe ideas. If a single ingredient is edible on its own (like 'Cake'), suggest serving it elegantly instead of forcing a gross mixture."
    )

    user_prompt = (
        f"User ingredients: {ingredients_str}. "
        "Create 1 to 3 different *edible and sensible* recipes using *only* these ingredients. "
        "If a combo is weird, output `is_possible: false`. "
        "Return a JSON object: "
        '{ "is_possible": true, "recipes": [ {"ingredients_used": ["..."], "name": "Recipe Name", "steps": ["..."], "time": "..."} ] }'
    )

    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL_NAME,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.6, # Lowered for more consistent logic
        )

        response_content = completion.choices[0].message.content
        recipe_data = json.loads(response_content)
        return recipe_data

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/submit-feedback")
async def submit_feedback(request: FeedbackRequest):
    try:
        data = {
            "recipe_name": request.recipe_name,
            "rating": request.rating,
            "comment": request.comment
        }
        
        # Log to file
        feedback_path = os.path.join("/tmp", "feedback.json")
        with open(feedback_path, "a") as f:
            f.write(json.dumps(data) + "\n")
        
        return {"status": "success", "message": "Feedback received. Thank you for helping me improve!"}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Serve static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(static_dir, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
