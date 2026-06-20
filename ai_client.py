import os
from google import genai


# CONFIGURATION

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash-lite"

if not GEMINI_API_KEY:
    print("Warning: Gemini API key not found.")


# CLIENT SETUP

client = genai.Client(api_key=GEMINI_API_KEY)


# AI FUNCTION

def ask_ai(prompt):
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config={
                "system_instruction": (
                    "You are an AI voice assistant similar to Alexa. "
                    "Speak naturally and briefly. Avoid long explanations."
                )
            }
        )

        return response.text

    except Exception as e:
        print(f"AI Error: {e}")
        return "Sorry, I could not connect to the AI."
