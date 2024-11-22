from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Replace with your actual API key
GEMINI_API_KEY = "AIzaSyDcaGNWa5kPsNkLiziIijPc__3VI4-DCW4"
print("we are here")
GEMINI_MODEL_NAME = "gemini-1.5-flash"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"

@app.route('/generate-dietary-requirements', methods=['POST'])
def generate_dietary_requirements():
    # Get health conditions from the JSON request body
    data = request.get_json()
    health_conditions = data.get("healthConditions", [])

    # Construct health conditions string
    health_conditions_text = ", ".join(health_conditions) if health_conditions else "no specific health conditions"

    # Set up the prompt for the Gemini API
    prompt_text = (
        f"Generate dietary recommendations based on the following health conditions: {health_conditions_text}. "
        f"Only return the output in this exact JSON format with no additional text, disclaimers, or explanations: \n"
        f"{{\n"
        f"  \"ingredientsuggestedtobeUsed\": [\"ingredient1\", \"ingredient2\", \"ingredient3\"],\n"
        f"  \"ingredientNottobeUsed\": [\"ingredient4\", \"ingredient5\"],\n"
        f"  \"energyMin\": number,\n"
        f"  \"energyMax\": number,\n"
        f"  \"carbohydratesMin\": number,\n"
        f"  \"carbohydratesMax\": number,\n"
        f"  \"fatMin\": number,\n"
        f"  \"fatMax\": number,\n"
        f"  \"proteinMin\": number,\n"
        f"  \"proteinMax\": number\n"
        f"}}"
    )

    # Prepare the payload for the Gemini API
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt_text}]
            }
        ]
    }

    # Set headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the API request
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        result = response.json()

        # Initialize dietary recommendations variables with default values
        ingredients_suggested = []
        ingredients_not_to_use = []
        energy_min = 0
        energy_max = 0
        carbohydrates_min = 0
        carbohydrates_max = 0
        fat_min = 0
        fat_max = 0
        protein_min = 0
        protein_max = 0

        # Check if the response has the expected structure
        if "candidates" in result:
            candidates = result["candidates"]
            if candidates:
                candidate = candidates[0]
                content = candidate.get("content", {})
                parts = content.get("parts", [])
                if parts:
                    dietary_recommendations = parts[0].get("text", "No recommendations generated.")
                    
                    # Check if the response is in a valid JSON format
                    try:
                        # If the response is not a valid JSON, it will be caught here
                        recommendations = json.loads(dietary_recommendations)  # Parse as JSON
                        
                        # Assign values to variables
                        ingredients_suggested = recommendations.get("ingredientsuggestedtobeUsed", [])
                        ingredients_not_to_use = recommendations.get("ingredientNottobeUsed", [])
                        energy_min = recommendations.get("energyMin", 0)
                        energy_max = recommendations.get("energyMax", 0)
                        carbohydrates_min = recommendations.get("carbohydratesMin", 0)
                        carbohydrates_max = recommendations.get("carbohydratesMax", 0)
                        fat_min = recommendations.get("fatMin", 0)
                        fat_max = recommendations.get("fatMax", 0)
                        protein_min = recommendations.get("proteinMin", 0)
                        protein_max = recommendations.get("proteinMax", 0)
                    
                    except json.JSONDecodeError:
                        return jsonify({"error": "Failed to parse dietary recommendations, invalid JSON."}), 500

        # Return the JSON response with assigned variables
        return jsonify({
            "dietaryRequirements": {
                "ingredientsuggestedtobeUsed": ingredients_suggested,
                "ingredientNottobeUsed": ingredients_not_to_use,
                "energyMin": energy_min,
                "energyMax": energy_max,
                "carbohydratesMin": carbohydrates_min,
                "carbohydratesMax": carbohydrates_max,
                "fatMin": fat_min,
                "fatMax": fat_max,
                "proteinMin": protein_min,
                "proteinMax": protein_max
            }
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=8888)
