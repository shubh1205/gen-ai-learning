# gen-ai-learning

This repository contains a collection of Python scripts that utilize the OpenAI API to perform various tasks. The scripts are designed to be run independently, and each script accepts an OpenAI API key as a named command-line argument.

## Setup and Installation

To get started, follow these steps:

1. **Create a virtual environment (venv) for your project:**

    ```bash
    python -m venv myenv
    ```

2. **Activate the virtual environment:**

    - On Linux/Mac:
  
      ```bash
      source myenv/bin/activate
      ```

    - On Windows:

      ```bash
      myenv\Scripts\activate
      ```

3. **Install the required Python packages from `requirements.txt`:**

    ```bash
    pip install -r requirements.txt
    ```

## Running the Scripts

All Python scripts in this repository accept an OpenAI API key as a named command-line argument. To run a script, use the following format:

    ```bash
    python script_name.py --api_key=YOUR_OPENAI_API_KEY
    ```
Replace script_name.py with the name of the script you want to run, and YOUR_OPENAI_API_KEY with your actual OpenAI API key.