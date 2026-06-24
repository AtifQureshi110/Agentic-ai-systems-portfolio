from dotenv import load_dotenv
from google import genai
import os 

load_dotenv()  # Load variables from .env
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY) 



def generate_response(prompt: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


if __name__ == "__main__":
    question = "What is Machine Learning? tell me just in 2 lines "
    answer = generate_response(question)

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(answer)