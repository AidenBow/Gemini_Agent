import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from call_function import available_functions, call_function

def main():
    load_dotenv()

    system_prompt = system_prompt = """
        You are a sassy but helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

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

    iterations = 0

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key = api_key)

    while True:
        iterations += 1
        #print(f'iteration: {iterations}\n')

        content = client.models.generate_content(
            model="gemini-2.0-flash-001", 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )

        for candidate in content.candidates:
            messages.append(candidate.content)
            print(f'candidate.content added: {candidate.content.parts[0].text}\n')

        if content.function_calls:
            for function_call_part in content.function_calls:
                messages.append(call_function(function_call_part))
                #print(f'funtion results added: {messages[-1]}')
        else:
            print(content.text)
            break

        if iterations >= 20:
            print("STOPPING: MAX ITERATIONS REACHED")
            break
    

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {content.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()