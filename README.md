# AI-agent-Fridge

🍳 **Your strict culinary assistant. Zero waste, infinite taste.**

A modern web application that uses AI to generate creative recipes based on the ingredients you have in your fridge. Stop wasting food and start cooking!

---

## 🎯 What It Does

The app answers the question: **"What can I cook with these ingredients?"**

Users enter ingredients they have, and an AI chef generates 1-3 recipe suggestions that use only (or mostly) those ingredients. The AI is "strict" about not making nonsensical combinations—it won't suggest weird mixes like "Cake and Tomato."

---

## 🏗️ Architecture

**Tech Stack:**
- **Backend**: FastAPI (Python) with Groq & OpenAI AI integrations
- **Frontend**: HTML, CSS, JavaScript with modern glassmorphic UI
- **Deployment**: Vercel (serverless)
- **Language Breakdown**: Python (30%), CSS (26.6%), JavaScript (25.8%), HTML (17.6%)

---

## 📁 Project Structure

```
├── api/
│   └── index.py          # FastAPI backend with recipe generation & feedback
├── static/
│   ├── index.html        # Main UI with glassmorphic design
│   ├── script.js         # Frontend logic & recipe rendering
│   └── style.css         # Modern styling with animations
├── fridge.py             # Legacy CLI version
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel deployment config
├── feedback.json        # User ratings/feedback storage
└── README.md            # Documentation
```

---

## ✨ Key Features

1. **Ingredient Input**: Users paste or type ingredients (comma-separated)
2. **Customization Options**:
   - 🌍 Cuisine type selection (Italian, Mexican, Indian, Chinese, etc.)
   - 🤖 AI model choice (GPT-4o, GPT-4o-Mini, LLaMA-3.3, Mixtral, Gemma 2)
   - 🧂 Toggle common spices/oils allowance
3. **Recipe Generation**: AI generates recipes in JSON format with:
   - Recipe name
   - Ingredients used
   - Step-by-step instructions
   - Estimated cooking time
4. **User Feedback**: Thumbs up/down rating system to improve AI
5. **Beautiful UI**: Modern glassmorphic design with smooth animations & icons

---

## 🔧 Backend API

### Generate Recipe
```http
POST /generate-recipe
Content-Type: application/json

{
  "ingredients": "tomato, cheese, bread",
  "provider": "openai:gpt-4o-mini",
  "nationality": "Italian",
  "allow_spices": true
}

Response:
{
  "is_possible": true,
  "recipes": [
    {
      "name": "Recipe Name",
      "ingredients_used": ["..."],
      "steps": ["..."],
      "time": "20 mins"
    }
  ]
}
```

### Submit Feedback
```http
POST /submit-feedback
Content-Type: application/json

{
  "recipe_name": "Cheesy Tomato Toast",
  "rating": 1,
  "comment": "Delicious!"
}

Response:
{
  "status": "success",
  "message": "Feedback received. Thank you for helping me improve!"
}
```

---

## 🚀 Live Demo

**🌐 Website**: [https://ai-agent-fridge.vercel.app](https://ai-agent-fridge.vercel.app)

---

## 💻 How It Works

1. User enters ingredients → Frontend sends to backend
2. Backend constructs intelligent system prompts for strict recipe generation
3. AI (GPT-4o-Mini by default, or Groq LLaMA as fallback) generates JSON recipes
4. Frontend renders recipes with interactive feedback buttons
5. User ratings are logged for continuous improvement

---

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- Node.js (optional, for frontend development)
- API keys: OpenAI and/or Groq

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/7H4N05/AI-agent-Fridge-.git
cd AI-agent-Fridge-
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create a `.env` file**
```env
OPENAI_API_KEY=your_openai_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

5. **Run the application**
```bash
python api/index.py
```

6. **Open in browser**
```
http://127.0.0.1:8000
```

### CLI Mode (Legacy)
```bash
python fridge.py
```

---

## 📦 Dependencies

- `fastapi` - Modern Python web framework
- `groq` - Groq AI API client
- `openai` - OpenAI API client
- `python-dotenv` - Environment variable management

---

## 🔑 Technologies Used

| Technology | Purpose |
|-----------|---------|
| **FastAPI** | High-performance backend framework |
| **Groq** | Fast open-source LLaMA models |
| **OpenAI** | GPT models for recipe generation |
| **Vercel** | Serverless deployment platform |
| **Lucide Icons** | Beautiful icon library |
| **Google Fonts** | Modern typography (Outfit) |

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Submit bug reports
- Suggest new features
- Improve documentation
- Create pull requests

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

Created by [@7H4N05](https://github.com/7H4N05)

---

**Happy Cooking! 🍽️** Use what you have, waste nothing, enjoy everything.
