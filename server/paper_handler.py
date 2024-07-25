import base64
import json
import os
from typing import Union

from pdf_parser import pdf_parser
from type import ChatRequest, PDFRequest
from utils import generate_embeddings, inference


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


def upload_pdf(pdf_request: PDFRequest, client):
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
    id, paper_name, docs = pdf_parser(file_path)

    # Gen embedding
    generate_embeddings(
        docs=docs, embedding_name=str(id), client=client
    )  # TODO: Merge generate embeddings
    # Remove the PDF file
    os.remove(file_path)

    return {
        "id": id,
        "author": "Unknown",
        "title": paper_name,
        "abstract": "Unknown",
    }


def get_or_create_chat_log(chat_id: int, question: str) -> dict:
    CHATDIR = f"./chat/{chat_id}"
    if not os.path.exists(CHATDIR):
        os.makedirs(CHATDIR)

    title = question[:10] + "..." if len(question) > 10 else question

    chat_log = {
        "metadata": {
            "id": chat_id,
            "title": title,
        },
        "chat": [],
    }

    chat_dir = os.path.join(CHATDIR, "chat.json")
    if not os.path.exists(chat_dir):
        with open(chat_dir, "w") as f:
            json.dump(chat_log, f, indent=4)

    with open(chat_dir, "r") as f:
        chat_log = json.load(f)

    return chat_log


def update(chat_log: dict, chat_id: int, question: str, inference_result: str):
    chat_log["chat"].append({"user": question, "model": inference_result})
    CHATDIR = f"./chat/{chat_id}"
    chat_log_path = os.path.join(CHATDIR, "chat.json")
    with open(chat_log_path, "w") as f:
        json.dump(chat_log, f, indent=4)


def chat(chat_request: ChatRequest):
    chat_id = chat_request.id
    question = chat_request.body
    chat_log = get_or_create_chat_log(chat_id, question)
    target_ids = [f"id{id}" for id in chat_request.refer]
    # inference_result = inference(question=question, embedding_names=target_ids)
    inference_result = "This is model's response"
    update(chat_log, chat_id, question, inference_result)
    return inference_result
