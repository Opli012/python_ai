import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()

    input_text = sys.argv[1:]

    if not input_text:
        print("AI Code Assistant")
        print('Usage: python main.py "your prompt here"\n')
        print('For detailed information add a --verbose flag.\n')
        sys.exit(1)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    print("Response:")
    print(generate_content(client, messages).text)

    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        print(f"User prompt: {user_prompt}\n")
        generate_details(generate_content(client, messages))


def generate_content(client, messages):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    return response

def generate_details(response):
    prompt_tokens = response.usage_metadata.prompt_token_count
    completion_tokens = response.usage_metadata.candidates_token_count

    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {completion_tokens}")


if __name__ == "__main__":
    main()