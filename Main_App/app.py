from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = "your_actual_gemini_api_key" # GENERATE YOUR OWN GEMINI API KEY AND ADD IT
GEMINI_MODEL_NAME = "gemini-1.5-flash-8b" 
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"

@app.route('/generate-diet-plan', methods=['POST'])
def generate_diet_plan():
    data = request.get_json()
    
    # Extract data from the request
    health_conditions = data.get("healthConditions", [])
    calories = data.get("calories", 1800)
    meals = data.get("meals", 3)
    regions = data.get("recipes", [])

    # Validate inputs
    if not health_conditions:
        return jsonify({"error": "Health conditions are required."}), 400
    if not regions:
        return jsonify({"error": "Preferred regions are required."}), 400

    # Constructing the input prompt
    conditions_text = ", ".join(health_conditions)
    regions_text = ", ".join(regions)
    prompt_text = (
        f"Create a meal plan with approximately {calories} calories, divided across {meals} meals per day. "
        f"The meals should be inspired by the following cuisines or regions: {regions_text}. "
        f"Ensure the meal plan accommodates these health conditions: {conditions_text}. "
        f"Focus on providing only the meals with no additional explanations or context."
    )

    # Payload for GEMINI API
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt_text}]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Sending the request to GEMINI API
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        # Extracting the generated dietary plan
        dietary_plan = ""
        if "candidates" in result:
            candidates = result["candidates"]
            if candidates:
                candidate = candidates[0]
                content = candidate.get("content", {})
                parts = content.get("parts", [])
                if parts:
                    dietary_plan = parts[0].get("text", "No dietary plan generated.")

        # Logging and returning the response
        print("Raw dietary plan:", dietary_plan)
        return jsonify({"dietPlan": dietary_plan})

    except requests.exceptions.RequestException as e:
        print("Request error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=8888)
