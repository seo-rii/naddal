# Client code to test the FastAPI endpoint
import requests
import base64
import json
import time

# Give the server a moment to start
time.sleep(1)

# Path to the PDF file you want to encode
pdf_file_path = "sample_pdfs/Attention Is All You Need.pdf"

# Read the PDF file and encode it in Base64
with open(pdf_file_path, "rb") as pdf_file:
    pdf_base64 = base64.b64encode(pdf_file.read()).decode("utf-8")

# Prepare the JSON payload
payload = {"file_name": "exam___ple.pdf", "file_data": pdf_base64}

# Define the URL of the FastAPI endpoint
url = "http://127.0.0.1:8000/api/paper"

# Send the Get request
response = requests.get(url)
print(response.json())

# Send the POST request
response = requests.post(
    url, headers={"Content-Type": "application/json"}, data=json.dumps(payload)
)

# Print the response from the server
print(response.status_code)
print(response.json())
