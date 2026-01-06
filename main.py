import os
import argparse

from google import genai
from google.genai import types # type: ignore
from dotenv import load_dotenv # type: ignore
from config import SYSTEM_PROMPT
from functions.call_funcs import available_functions, call_function


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
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT),
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
    function_call_responses= []

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables.")

    client = genai.Client(api_key=api_key)

    response = generate_response(client, messages)

    if response.function_calls:
        for func_call in response.function_calls:
            if (
                func_call.name == "get_files_info"
                and func_call.args is not None
                and "directory" not in func_call.args
            ):
                func_call.args["directory"] = "."
            
            function_call_result = call_function(func_call, verbose=args.verbose)
            if not function_call_result.parts:
                raise Exception("No parts list in function call result.")
            if not function_call_result.parts[0].function_response:
                raise Exception("No response in function call result of parts list.")
            if not function_call_result.parts[0].function_response.response:
                raise Exception("No content in response of function call result.")
            
            function_call_responses.append(function_call_result.parts[0])
            
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

    else:
        print("------------------------------")
        if args.verbose is True: 
            verbose_handler(response, args.user_prompt)
        print(f"Response text: {response.text}")
        print("------------------------------")


if __name__ == "__main__":
    main()
