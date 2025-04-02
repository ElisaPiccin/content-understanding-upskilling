"""
This script performs the following steps:

1. Submits an HTTP POST request to the Content Understanding endpoint to analyze a document using the 'travel-insurance-analyzer'.
    - The document is specified by its URL.
    - The POST request retrieves an operation ID for tracking the analysis.

2. Repeatedly submits an HTTP GET request to check the status of the analysis operation.
    - Continues polling until the operation is no longer running.

3. If the analysis operation succeeds:
    - Retrieves and displays the JSON response in a formatted manner.

For testing the script run: 
python analyze_doc.py

or, if you want to write the output to a file, run:
python analyze_doc.py > output.txt
"""

import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(override=True)

endpoint = os.getenv('AZURE_CU_ENDPOINT')
key = os.getenv('AZURE_CU_KEY')

analyzer_name = os.getenv('AZURE_CU_ANALYZER_NAME') # e.g. 'my-invoice-analyzer'
document_url = 'https://raw.githubusercontent.com/Azure/azure-sdk-for-python/main/sdk/formrecognizer/azure-ai-formrecognizer/tests/sample_forms/forms/Invoice_1.pdf' 
cu_version = '2024-12-01-preview'

body = {
    "url": document_url
}

headers = {
    "Ocp-Apim-Subscription-Key": key,
    "Content-Type": "application/json"
}

url = endpoint + f'contentunderstanding/analyzers/{analyzer_name}:analyze?api-version={cu_version}'

print ('Analyzing document...')
response = requests.post(url, headers=headers, data=json.dumps(body))

print(response.status_code)
response_json = response.json()

# Extract the "id" value from the response
id_value = response_json.get("id")

# Perform a GET request t get the results
print ('Getting results...')
result_url = f'{endpoint}contentunderstanding/analyzers/{analyzer_name}/results/{id_value}?api-version={cu_version}'
result_response = requests.get(result_url, headers=headers)
print(result_response.status_code)

status = result_response.json().get("status")
while status == "Running":
    print('...')
    result_response = requests.get(result_url, headers=headers)
    status = result_response.json().get("status")

if status == "Succeeded":
    print("Analysis succeeded.")
    results = result_response.json()
    # Print formatted JSON with indentation
    print(json.dumps(results, indent=2))