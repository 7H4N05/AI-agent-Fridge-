document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-btn');
    const ingredientsInput = document.getElementById('ingredients');
    const resultSection = document.getElementById('result-section');

    generateBtn.addEventListener('click', async () => {
        const ingredients = ingredientsInput.value.trim();

        if (!ingredients) {
            alert('Please enter some ingredients first!');
            return;
        }

        // Set loading state
        generateBtn.classList.add('loading');
        generateBtn.disabled = true;

        try {
            const response = await fetch('/generate-recipe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ ingredients }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to generate recipe');
            }

            const data = await response.json();
            renderResult(data);

        } catch (error) {
            console.error('Error:', error);
            alert('Oops! Something went wrong: ' + error.message);
        } finally {
            generateBtn.classList.remove('loading');
            generateBtn.disabled = false;
        }
    });

    function renderResult(data) {
        resultSection.innerHTML = '';
        resultSection.classList.remove('hidden');

        if (!data.is_possible || !data.recipes || data.recipes.length === 0) {
            resultSection.innerHTML = `
                <div class="glass-card no-recipe">
                    <i data-lucide="frown"></i>
                    <h2>No Edible Dish Possible</h2>
                    <p>I couldn't create any strict recipes with just those ingredients. Maybe add a few more staples?</p>
                </div>
            `;
        } else {
            // Create a container for multiple cards if needed
            const cardsHtml = data.recipes.map((recipe, index) => `
                <div class="glass-card recipe-card" data-index="${index}">
                    <h2 class="recipe-title">${recipe.name}</h2>
                    
                    <div class="recipe-meta">
                        <div class="meta-item">
                            <i data-lucide="clock"></i>
                            <span>${recipe.time}</span>
                        </div>
                        <div class="meta-item">
                            <i data-lucide="shopping-basket"></i>
                            <span>${recipe.ingredients_used.length} Ingredients</span>
                        </div>
                    </div>

                    <div class="recipe-content">
                        <div class="ingredients-list" style="margin-bottom: 30px;">
                            <h3 class="section-title"><i data-lucide="clipboard-list"></i> Ingredients</h3>
                            <ul class="list-container">
                                ${recipe.ingredients_used.map(ing => `<li class="list-item">${ing}</li>`).join('')}
                            </ul>
                        </div>

                        <div class="steps-list">
                            <h3 class="section-title"><i data-lucide="list-ordered"></i> Instructions</h3>
                            <ul class="list-container">
                                ${recipe.steps.map((step, index) => `<li class="list-item"><strong>${index + 1}.</strong> ${step}</li>`).join('')}
                            </ul>
                        </div>
                    </div>

                    <div class="feedback-section">
                        <p class="feedback-prompt">How was this recipe?</p>
                        <div class="feedback-buttons">
                            <button class="feedback-btn up" onclick="handleFeedback('${recipe.name}', 1, ${index})">
                                <i data-lucide="thumbs-up"></i>
                            </button>
                            <button class="feedback-btn down" onclick="handleFeedback('${recipe.name}', -1, ${index})">
                                <i data-lucide="thumbs-down"></i>
                            </button>
                        </div>
                        <div id="feedback-msg-${index}" class="feedback-success hidden">Thanks for your feedback!</div>
                    </div>
                </div>
            `).join('');

            resultSection.innerHTML = cardsHtml;
        }

        // Re-create icons for the newly added elements
        lucide.createIcons();
        
        // Scroll to result
        resultSection.scrollIntoView({ behavior: 'smooth' });
    }
});

async function handleFeedback(recipeName, rating, index) {
    const msgEl = document.getElementById(`feedback-msg-${index}`);
    const buttonsEl = document.querySelector(`.recipe-card[data-index="${index}"] .feedback-buttons`);
    
    try {
        const response = await fetch('/submit-feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ recipe_name: recipeName, rating: rating })
        });
        
        if (response.ok) {
            buttonsEl.classList.add('hidden');
            msgEl.classList.remove('hidden');
        }
    } catch (error) {
        console.error('Feedback error:', error);
    }
}
