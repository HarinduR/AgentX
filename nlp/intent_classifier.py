# nlp/intent_classifier.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def classify_intent(message: str) -> dict:

    system_prompt = (
        "You are a helpful assistant that classifies customer complaints. "
        "Given a complaint, identify the following:\n"
        "- intent (e.g., product_issue, delivery_delay, payment_issue, general_query)\n"
        "- urgency level (low, medium, high)\n"
        "Return as JSON with keys: intent, urgency"
    )

    user_prompt = f"Complaint: {message}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.3,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        # Extract response text
        reply = response.choices[0].message['content']
        
        # Parse it as a dictionary (safe way)
        import json
        result = json.loads(reply)
        return result

    except Exception as e:
        print(f"[ERROR] OpenAI intent classification failed: {e}")
        return {"intent": "unknown", "urgency": "unknown"}
