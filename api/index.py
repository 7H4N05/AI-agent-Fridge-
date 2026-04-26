import os
import json
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from openai import OpenAI
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

# Initialize clients globally
openai_key = os.getenv("OPENAI_API_KEY")
if openai_key and openai_key != "your_openai_api_key_here":
    openai_client = OpenAI(api_key=openai_key)
    OPENAI_MODEL_NAME = "gpt-4o-mini" # User preferred model
else:
    openai_client = None

groq_key = os.getenv("GROQ_API_KEY")
if groq_key:
    groq_client = Groq(api_key=groq_key)
    GROQ_MODEL_NAME = "llama-3.3-70b-versatile"
else:
    groq_client = None

class RecipeRequest(BaseModel):
    ingredients: str
    provider: Optional[str] = "openai"
    nationality: Optional[str] = "Any"
    allow_spices: Optional[bool] = False

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
    nationality = request.nationality
    allow_spices = request.allow_spices
    
    if not ingredients_str:
        raise HTTPException(status_code=400, detail="Please enter some ingredients.")

    nationality_clause = f"Cuisine Type: The recipes should be inspired by {nationality} culinary traditions. " if nationality and nationality.lower() != "any" else ""

    spice_rule = (
        "Strict Rule: You may freely use common pantry items like salt, pepper, cooking oil, water, and basic dry spices even if they are not explicitly listed in the ingredients. "
        if allow_spices else
        "Strict Rule: Use *only* the ingredients provided. Do NOT add salt, pepper, oil, water, or anything else unless explicitly listed. "
    )

    system_instruction = (
        "You are an elite, highly-trained professional chef AI. Your mission is to create recipes that are not only strict but also *delicious* and *culinary-logical*. "
        f"{spice_rule}"
        "Culinary Rule: You must ensure the combination actually makes sense. Do NOT suggest disgusting or nonsensical combinations (like 'Cake and Tomato'). "
        "Logic: If the ingredients provided are fundamentally incompatible, return `is_possible: false`. "
        f"{nationality_clause}"
        "Goal: Provide 1-3 distinct, high-quality recipe ideas. If a single ingredient is edible on its own (like 'Cake'), suggest serving it elegantly instead of forcing a gross mixture."
    )

    user_prompt = (
        f"User ingredients: {ingredients_str}. "
        "Create 1 to 3 different *edible and sensible* recipes using *only* these ingredients. "
        "If a combo is weird, output `is_possible: false`. "
        "Return a JSON object: "
        '{ "is_possible": true, "recipes": [ {"ingredients_used": ["..."], "name": "Recipe Name", "steps": ["..."], "time": "..."} ] }'
    )

    # Parse the provider and model_name
    if ":" in request.provider:
        provider_name, model_name = request.provider.split(":", 1)
    else:
        provider_name = request.provider
        model_name = ""

    if provider_name == "groq" and groq_client:
        active_client = groq_client
        active_model = model_name or GROQ_MODEL_NAME
    elif provider_name == "openai" and openai_client:
        active_client = openai_client
        active_model = model_name or OPENAI_MODEL_NAME
    else:
        # Fallback to whatever is available
        if openai_client:
            active_client = openai_client
            active_model = OPENAI_MODEL_NAME
        elif groq_client:
            active_client = groq_client
            active_model = GROQ_MODEL_NAME
        else:
            raise HTTPException(status_code=500, detail="No AI provider configured.")

    try:
        completion = active_client.chat.completions.create(
            model=active_model,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
            # Removed temperature=0.6 because gpt-5-nano doesn't support custom temperatures
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
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(static_dir, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
