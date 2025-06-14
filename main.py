import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

def main():
    load_dotenv()

    user_prompt = sys.argv[1:]

    if not user_prompt:
        user_prompt = input("enter your prompt here: ")
        #sys.exit(1)
    user_prompt = " ".join(user_prompt)

    if "--verbose" in user_prompt:
        verbose = True
        user_prompt = user_prompt.replace("--verbose", "")
    else:
        verbose = False

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key = api_key)

    content = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages)
    print(content.text)
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {content.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()