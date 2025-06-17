import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

verbose = False

if len(sys.argv) < 2:
    print("error: prompt not provided")
    sys.exit(1)
if len(sys.argv) == 3:
    if sys.argv[2] == "--verbose":
        verbose = True

user_prompt = sys.argv[1]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key= api_key)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
    model="gemini-2.0-flash-001", contents=messages
)

if verbose == True:
    print(f"User prompt: {user_prompt}")

print(response.text)
if verbose == True: 
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}"
    )
