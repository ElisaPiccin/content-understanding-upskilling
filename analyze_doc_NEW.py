"""
IMPORTANT:
assign the user who runs this script the "Cognitive Services User" role in the Azure portal for the Azure AI Services resource.

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
python analyze_doc_NEW.py > output.txt
"""

import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(override=True)

# Check the original sample files here: https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/formrecognizer/azure-ai-formrecognizer/tests/sample_forms
# document_url = 'https://raw.githubusercontent.com/Azure/azure-sdk-for-python/main/sdk/formrecognizer/azure-ai-formrecognizer/tests/sample_forms/forms/Invoice_1.pdf' 
document_url = 'https://raw.githubusercontent.com/Azure/azure-sdk-for-python/main/sdk/formrecognizer/azure-ai-formrecognizer/tests/sample_forms/forms/sample_invoice.jpg' 

endpoint = os.getenv('AZURE_CU_ENDPOINT_NEW')
key = os.getenv('AZURE_CU_KEY_NEW')

analyzer_name = os.getenv('AZURE_CU_ANALYZER_NAME_NEW') # e.g. 'my-invoice-analyzer'
cu_version = os.getenv('AZURE_CU_API_VERSION_NEW') # '2024-12-01-preview'

print('Endpoint:', endpoint)
print('Analyzer Name:', analyzer_name)
print('Document URL:', document_url)
print('API Version:', cu_version)

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

# NB: the result URL is different in the new API version
# result_url = f'{endpoint}contentunderstanding/analyzers/{analyzer_name}/results/{id_value}?api-version={cu_version}'
result_url = f"{endpoint}/contentunderstanding/analyzerResults/{id_value}?api-version={cu_version}"
result_response = requests.get(result_url, headers=headers)
print(result_response.status_code)

status = result_response.json().get("status")
while status == "Running":
    print('...')
    result_response = requests.get(result_url, headers=headers)
    status = result_response.json().get("status")

print('Final status:', status)

if status == "Succeeded":
    print("Analysis succeeded.")
    results = result_response.json()
    # Print formatted JSON with indentation
    print(json.dumps(results, indent=2))