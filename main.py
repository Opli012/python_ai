import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import call_function, available_functions

from prompts import system_prompt
from config import MAX_ITERATIONS


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('Usage: python main.py "your prompt here"\n')
        print('For detailed information add a --verbose flag.\n')
        sys.exit(1)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    done = False
    for i in range(MAX_ITERATIONS):
        if done:
            break
        messages, done = generate_content(client, messages, verbose)
    else:
        print(f"Maximum iterations ({MAX_ITERATIONS}) reached.")
        sys.exit(1)


def generate_content(client, messages, verbose):
    model_name = "gemini-2.0-flash-001"
    
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    for candidate in response.candidates:
        messages.append(candidate.content)

    if not response.function_calls:
        print("Final response:\n")
        print(response.text)
        return messages, True

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("Empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("No function responses generated, exiting.")

    messages.append(types.Content(role="tool", parts=function_responses))

    return messages, False


if __name__ == "__main__":
    main()