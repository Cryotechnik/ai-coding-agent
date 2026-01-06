import argparse
import os

from config import AGENT_LOOP_LIMIT, SYSTEM_PROMPT, MODEL
from dotenv import load_dotenv # type: ignore
from functions.call_funcs import available_functions, call_function
from google import genai
from google.genai import types # type: ignore


def parse_args():
    parser = argparse.ArgumentParser(description="AI Code Assistant using Gemini API")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()


def build_messages(user_prompt):
    return [types.Content(role="user", parts=[types.Part(text=user_prompt)])]


def generate_response(client, messages):
    response = client.models.generate_content(
        model=MODEL,
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT),
    )
    
    if response.usage_metadata is None:
        raise RuntimeError("Usage metadata is missing in the response.")
    
    return response


def extract_function_response_part(function_call_result: types.Content):
    if not function_call_result.parts:
        raise ValueError("No parts in function call result")

    part = function_call_result.parts[0]

    if not part.function_response:
        raise ValueError("Missing function_response on first part")

    if not part.function_response.response:
        raise ValueError("Missing response content in function_response")

    return part


def verbose_handler(response):
    if not response.usage_metadata:
        return
    print("------------------------------")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


def main():
    args = parse_args()
    messages = build_messages(args.user_prompt)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables.")

    client = genai.Client(api_key=api_key)

    for _ in range(AGENT_LOOP_LIMIT):

        response = generate_response(client, messages)

        candidates = response.candidates or []
        for candidate in candidates:
            messages.append(candidate.content)

        function_call_responses = []

        if response.function_calls:
            for func_call in response.function_calls:
                if func_call.name == "get_files_info":
                    func_args = func_call.args or {}
                    func_args.setdefault("directory", ".")
                    func_call.args = func_args
                
                function_call_result = call_function(func_call, verbose=args.verbose)
                
                part = extract_function_response_part(function_call_result)
                
                function_call_responses.append(part)
                
                if args.verbose:
                    print(f"-> {part.function_response.response}")

            messages.append(types.Content(role="user", parts=function_call_responses))

        else:
            print("------------------------------")
            print(f"Response text: {response.text}")
            if args.verbose: 
                verbose_handler(response)
            print("------------------------------")
            return
        
    raise RuntimeError("Reached agent loop limit without a final response.")

if __name__ == "__main__":
    main()
