import json
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file in the same folder
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Get the business card schema
with open("2025-05-01-preview/card.json", "r") as file:
    schema_json = json.load(file)

# Use a PUT request to submit the schema for a new analyzer
analyzer_name = "business_card_analyser_procode_v1"
print(f"Creating analyzer: {analyzer_name}")

# Read subscription key and endpoint from environment variables
api_key = os.getenv("AZURE_CU_KEY")
endpoint = os.getenv("AZURE_CU_ENDPOINT")
api_version = os.getenv("AZURE_CU_API_VERSION", "2025-05-01-preview")
print(f"Using endpoint: {endpoint}")
print(f"Using API version: {api_version}")

headers = {
    "Ocp-Apim-Subscription-Key": api_key,
    "Content-Type": "application/json"}

url = f"{endpoint}/contentunderstanding/analyzers/{analyzer_name}?api-version={api_version}"

response = requests.put(url, headers=headers, data=json.dumps(schema_json))

# Get the response and extract the ID assigned to the operation
callback_url = response.headers["Operation-Location"]

# Use a GET request to check the status of the operation
result_response = requests.get(callback_url, headers=headers)

# Keep polling until the operation is complete
status = result_response.json().get("status")
while status == "Running":
    result_response = requests.get(callback_url, headers=headers)
    status = result_response.json().get("status")

print("Done!")