import json
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file in the same folder
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Read the image data
input_file = "2025-05-01-preview/business_card.png"
with open(input_file, "rb") as file:
        image_data = file.read()
    
## Use a POST request to submit the image data to the analyzer
analyzer_name = "business_card_analyser_procode"
print(f"Using analyzer: {analyzer_name}")

# Read subscription key and endpoint from environment variables
api_key = os.getenv("AZURE_CU_KEY")
endpoint = os.getenv("AZURE_CU_ENDPOINT")
api_version = os.getenv("AZURE_CU_API_VERSION", "2025-05-01-preview")
print(f"Using endpoint: {endpoint}")
print(f"Using API version: {api_version}")

headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/octet-stream"}

url = f"{endpoint}/contentunderstanding/analyzers/{analyzer_name}:analyze?api-version={api_version}"

response = requests.post(url, headers=headers, data=image_data)

# Get the response and extract the ID assigned to the analysis operation
response_json = response.json()
id_value = response_json.get("id")

# Use a GET request to check the status of the analysis operation
result_url = f"{endpoint}/contentunderstanding/analyzerResults/{id_value}?api-version={api_version}"

result_response = requests.get(result_url, headers=headers)

# Keep polling until the analysis is complete
status = result_response.json().get("status")
while status == "Running":
        result_response = requests.get(result_url, headers=headers)
        status = result_response.json().get("status")

# Get the analysis results
if status == "Succeeded":
    result_json = result_response.json()
    print("Analysis completed successfully.")
    # print the analysis results
    print(json.dumps(result_json, indent=2))
    # save results to a file
    with open("2025-05-01-preview/business_card_analysis_result.json", "w") as result_file:
        json.dump(result_json, result_file, indent=2)
        # if inpyt_file contains business_card.png, print the fields
    if str(input_file).endswith("business_card.png"):
        # Iterate through the fields and extract the names and type-specific values
        print("\n\nExtracted fields:")
        contents = result_json["result"]["contents"]
        for content in contents:
            if "fields" in content:
                fields = content["fields"]
                for field_name, field_data in fields.items():
                    if field_data['type'] == "string":
                        print(f"{field_name}: {field_data['valueString']}")