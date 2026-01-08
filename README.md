# AI Code Assistant (Google Gemini Powered)

A command-line AI agent capable of writing, analyzing, and executing code locally. This tool utilizes Google's Gemini 2.5 Flash model to perform agentic workflows, allowing it to list files, read content, write code, and run Python scripts autonomously within a safe environment. This project was built as part of the Computer Science curriculum at [Boot.dev](https://boot.dev).

**⚠️ SECURITY WARNING: USE AT YOUR OWN RISK**

This program gives an AI model direct read, write, and execute permissions on your file system. Unlike professional production agents, this educational project **does not** contain advanced sandboxing or safety guardrails.

* **Potential for Data Loss:** The AI has the ability to overwrite or modify files without confirmation.
* **Directory Restriction:** You **must** ensure the `WORKING_DIRECTORY` in `config.py` is set to an isolated folder (a sandbox). **Never** run this tool in your root directory, system folders, or any directory containing sensitive or irreplaceable data.
* **Review Code:** Do not use this tool unless you understand how the code works.

## Features

* **File System Navigation:** Can list files and directories to understand project structure (`get_files_info`).
* **File Operations:** Can read (`get_file_content`) and writes (`write_file`) code or text files.
* **Code Execution:** Can execute Python scripts (`run_python_file`) and analyze the output (stdout/stderr) to debug or verify logic.
* **Agentic Loop:** Uses an iterative loop to think, act, and observe results until the task is complete.
* **Safety Limits:** Constrained within a set working directory and by an agent loop limit and file character reading limits.

## Prerequisites

* Python 3.10+
* A Google Gemini API Key

## Configuration

1. **Environment Setup:**
    Create a `.env` file in the root directory and add your API key:
    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    ```

2. **Change Variables in Config.py:**
    * **`WORKING_DIRECTORY`**: This is the "sandbox" where the AI is allowed to read/write files.
        * *Default:* `./calculator`
        * *Action:* Change this to the path of the specific project folder you want the AI to work on.
    * **`AGENT_LOOP_LIMIT`**: The maximum number of steps the AI can take (prevents infinite loops).
        * *Default:* `20`
    * **`MODEL`**: The specific Gemini model version.
        * *Default:* `gemini-2.5-flash`

## Usage

Run the main script from your terminal with a prompt describing what you want the AI to do.

**Basic Command:**
python main.py "Request for agent"

**Verbose Mode**
Use the --verbose flag to see the tool calls and token usage.

## Quick Start: Calculator Demo

To help you safely test the agent, this project includes a pre-made calculator program located in the `./calculator` directory provided by Boot.dev.

1.  **Verify Configuration:**
    Ensure your working directory points to this demo folder (it should by default):
    ```config.py
    WORKING_DIRECTORY = "./calculator"
    ```

2. **Mess Something Up in the Calculator**
    The calculator is currently set up correctly. Open the `./calculator/pkg/calculator.py` file and purposefully mess with it by changing something small like removing the multiplication operator.

3.  **Run a Test Command:**
    Try asking the agent to add a feature or fix a bug in the provided code:
    ```bash
    python main.py "The calculator is missing multiplication. Please analyze the code and add a multiply function."
    ```