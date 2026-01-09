import json 
import ollama 
from app.ai.prompts import INTENT_CLASSIFICATION_PROMPT

model_name = "llama3.2:latest"

def classify_email_intent(email_text : str)-> dict : 
    """
    Classify email intent using ollama 
    Returns : 
    {
       "intent" : str,
       "confidence" : float
    }
    """

    prompt = INTENT_CLASSIFICATION_PROMPT.format(
        email_text = email_text[:4000]
    )

    try : 
        response = ollama.chat(
            model = model_name,
            messages= [ 
                {
                    "role" : "user",
                    "content" : prompt
                }
            ], 
            options={
                "temperature" : 0
            }
        )

        content = response['message']['content'].strip()

        return json.loads(content)
    
    except Exception as e : 
        return {
            "intent" : "unknown",
            "confidence" : 0.0,
            "error" : str(e)
        }
