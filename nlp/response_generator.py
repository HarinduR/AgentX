# nlp/response_generator.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(user_message: str, intent_data: dict) -> str:

    prompt = (
        "You are a friendly support assistant. Based on the customer's message and the detected intent, "
        "generate a helpful and reassuring reply. Keep it short and clear.\n\n"
        f"Complaint: {user_message}\n"
        f"Intent: {intent_data.get('intent')}\n"
        f"Urgency: {intent_data.get('urgency')}\n"
        "Reply:"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.5,
            messages=[
                {"role": "system", "content": "You generate replies to customer complaints."},
                {"role": "user", "content": prompt}
            ]
        )

        reply = response.choices[0].message['content'].strip()
        return reply

    except Exception as e:
        print(f"[ERROR] Response generation failed: {e}")
        return "Sorry, we encountered an issue while processing your request."

