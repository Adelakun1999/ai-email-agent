import ollama
from app.ai.prompts import RESPONSE_PROMPTS

def generate_draft_response(intent:str , email_text:str) -> str | None : 
    if intent not in RESPONSE_PROMPTS:
        return None 
    
    prompt = RESPONSE_PROMPTS[intent].format(
        email_text = email_text
    )

    response = ollama.chat(
        model = "llama3.2:latest",
        messages= [
            {"role" : "user", "content" : prompt}
        ]
    )

    return response['message']['content'].strip()

