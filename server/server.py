import base64
import os
from typing import Union, List
from utils import generate_embeddings, inference
from paper_handler import get_paper_list
from fastapi import FastAPI, HTTPException, Query
from paper_handler import upload_pdf
from type import PDFRequest

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/generate_embeddings/{filepath:path}/{embedding_name}")
def generate_embed(filepath, embedding_name: str):
    generate_embeddings(pdf_filepath=filepath, embedding_name=embedding_name)


@app.get("/api/inference/{question}")
def run_inference(question, names: List[str] = Query(...)):
    return {"output": inference(question=question, embedding_names=names)}


@app.get("/api/paper")
def get_paper():
    return get_paper_list()


@app.post("/api/paper")
def decode_pdf(pdf_request: PDFRequest):
    try:
        result = upload_pdf(pdf_request=pdf_request)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
