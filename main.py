import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content

def main():
    load_dotenv()

    system_prompt = system_prompt = """
        You are a sassy but helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """
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

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content
        ]
    )  

    content = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

    if not content.function_calls: #this prevents a warning from non-text items created by function calls
        print(content.text)

    for function_call_part in content.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {content.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()