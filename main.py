import os
import sys
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()

    input_text = sys.argv[1:]

    if not input_text:
        print("AI Code Assistant")
        print('Usage: python main.py "your prompt here"\n')
        sys.exit(1)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    prompt_text = sys.argv[1]
    print(f"Received input: {prompt_text}")

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents={prompt_text}
    )
    print(response.text)

    prompt_tokens = response.usage_metadata.prompt_token_count
    completion_tokens = response.usage_metadata.candidates_token_count

    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {completion_tokens}")


if __name__ == "__main__":
    main()