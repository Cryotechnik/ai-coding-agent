# Maximum number of tool-execution cycles allowed per user request to prevent infinite loops.
AGENT_LOOP_LIMIT = 20

# Safety cap on the number of characters read from a file to prevent token overflow.
MAX_CHARS_LIMIT = 10000

# The specific identifier for the Gemini API model version being utilized.
MODEL = "gemini-2.5-flash"

# The foundational instructions defining the AI's persona, capabilities, and operational constraints.
SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# The local root path where all file system operations are securely confined.
WORKING_DIRECTORY = "./calculator"
