# content-understanding-upskilling
The content of this repository is intended for **training purposes only**.

- **`analyze_doc.py`**: Script to submit a document url to an analyzer using the Content Understanding REST APIs.
- **`analyze_doc_file_path.py`**: Handles document url and local file paths as document to submit to the analyzer through REST APIs.
- **`client_quickstart.py`**: Example script demonstrating client authentication (starting from the code snippet provided in the Azure AI Foundry UI).
- **`management.ipynb`**: utilities for analyzers lifecycle management.
- **`env.txt`**: Template for `.env` file with placeholders for required environment variables.
- **`requirements.txt`**: List of Python dependencies required for the project.

## Enhanced RAG

- **`search_with_visual_document.ipynb`**: End-to-end example to enrich Document Intelligence output with Content Understanding and leverage it as a Knowledge Base.
- **`requirements_aisearch.txt`**: Extended list of Python dependencies required for the enhanced RAG scenario.


## Setting up the Conda Environment

To create a conda environment called `cu-upskilling` with Python 3.10, follow these steps:

1. Open your terminal or command prompt.
2. Run the following command to create the environment:

    ```sh
    conda create --name cu-upskilling python=3.13
    ```

3. Activate the newly created environment:

    ```sh
    conda activate cu-upskilling
    ```

4. Install the required dependencies from [requirements.txt](requirements.txt):

    ```sh
    pip install -r requirements.txt
    ```

