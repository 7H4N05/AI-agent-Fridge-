"""
Fridge AI Agent - Legacy Script
This script has been upgraded to a modern web application.

To run the new web app:
1. Run: python main.py
2. Open: http://127.0.0.1:8000 in your browser.
"""

import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_recipe_cli(ingredients_str: str):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    model = "llama-3.3-70b-versatile"

    system_instruction = (
        "You are a strict culinary AI assistant. Use *only* the provided ingredients."
    )
    
    user_prompt = f"Ingredients: {ingredients_str}. Provide a recipe name and steps."

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ]
        )
        print(completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Fridge AI CLI Mode")
    print("-" * 20)
    user_input = input("Enter ingredients (separated by commas): ")
    if user_input:
        generate_recipe_cli(user_input)
    else:
        print("No ingredients provided. Run 'python main.py' for the full experience!")