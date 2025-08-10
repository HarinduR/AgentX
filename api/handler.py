# api/handler.py

from nlp.intent_classifier import classify_intent
from nlp.response_generator import generate_response

def handle_complaint(user_id: str, message: str) -> dict:

    print(f"[INFO] Received complaint from {user_id}: {message}")
    
    # Step 1: Classify intent
    intent_data = classify_intent(message)
    print(f"[DEBUG] Intent data: {intent_data}")
    
    # Step 2: Generate AI-based response
    final_response = generate_response(message, intent_data)
    
    # Output structure
    return {
        "user_id": user_id,
        "intent": intent_data.get("intent"),
        "urgency": intent_data.get("urgency"),
        "response": final_response
    }
