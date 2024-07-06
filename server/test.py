# Client code to test the FastAPI endpoint
import os
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
# response = requests.get(url)
# print(response.json())

# Send the POST request
response = requests.post(
    url, headers={"Content-Type": "application/json"}, data=json.dumps(payload)
)

# Print the response from the server
print(response.status_code)
print(response.json())


def get_paper_by_id(paper_id: int, save_path: str = "./uploads"):
    # Get paper by id from ./uploads dir
    paper_list = os.listdir(save_path)
    if paper_id > len(paper_list):
        return None
    else:
        for file in paper_list:
            if file.startswith("."):
                continue
            title, extracted_id = file.split("_")
            extracted_id = int(extracted_id)
            if extracted_id == paper_id:
                with open(f"{save_path}/{file}/parsed.html", "r") as f:
                    raw = f.read()
                information = {"id": extracted_id, "title": title, "raw": raw}
                return information
    return None
