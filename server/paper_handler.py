import base64
import codecs
import os
from typing import Union

from pdf_parser import pdf_parser
from type import PDFRequest


def get_paper_list():
    # Get paper list from ./uploads dir
    paper_list = []
    for file in os.listdir("./uploads"):
        if not file.startswith("."):
            title, id = file.split("_")
            information = {
                "id": id,
                "title": title,
                "author": "Unknown",
                "abstract": "Unknown",
            }
            paper_list.append(information)
    return paper_list


def get_paper_by_id(paper_id: int, save_path: str = "./uploads") -> Union[dict, None]:
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


def generate_embeddings(pdf_filepath, embedding_name):
    """
    Generate Embeddings for the given pdf, return 1 if success otherwise return 0
    params
    - pdf_filepath (base64_url): a string which is encoded from pdf
    - embedding_name (str): the name of the embedding
    """
    with open(f"./pdfs/{embedding_name}.pdf", "wb") as f:
        f.write(codecs.decode(pdf_filepath, "base64"))
    pdf_filepath = f"./pdfs/{embedding_name}.pdf"
    print(f"your pdf file is in {pdf_filepath}")


def upload_pdf(pdf_request: PDFRequest):
    # Decode the base64 file data
    file_data = base64.b64decode(pdf_request.file_data)

    # Define the file path
    file_name = pdf_request.file_name.replace("_", "-")
    file_path = os.path.join("tmp", file_name)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Write the decoded data to a PDF file
    with open(file_path, "wb") as pdf_file:
        pdf_file.write(file_data)

    # Parse the PDF file
    id, paper_name = pdf_parser(file_path)

    # Remove the PDF file
    os.remove(file_path)

    return {
        "id": id,
        "author": "Unknown",
        "title": paper_name,
        "abstract": "Unknown",
    }
