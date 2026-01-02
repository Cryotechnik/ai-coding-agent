import os
import argparse

from google import genai
from google.genai import types # type: ignore
from dotenv import load_dotenv # type: ignore

def parse_args():
    parser = argparse.ArgumentParser(description="AI Code Assistant using Gemini API")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()


def build_messages(user_prompt):
    return [types.Content(role="user", parts=[types.Part(text=user_prompt)])]


def generate_response(client, messages):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
    )
    
    if response.usage_metadata is None:
        raise RuntimeError("Usage metadata is missing in the response.")
    
    return response

def verbose_handler(response, user_prompt):
    print(f"User prompt: {user_prompt}")
    print("------------------------------")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("------------------------------")

def main():
    args = parse_args()
    messages = build_messages(args.user_prompt)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables.")

    client = genai.Client(api_key=api_key)

    response = generate_response(client, messages)

    print("------------------------------")
    if args.verbose is True: 
        verbose_handler(response, args.user_prompt)
    print(f"Response text: {response.text}")
    print("------------------------------")

if __name__ == "__main__":
    main()
