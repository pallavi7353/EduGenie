from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
key = os.environ.get("GEMINI_API_KEY")
print("Key found:", key[:10], "...")

try:
    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents="say hello in one word"
    )
    print("✅ SUCCESS! Gemini says:", response.text)
except Exception as e:
    print("❌ ERROR:", str(e)[:200])
