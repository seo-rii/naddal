from typing import Union, List
from utils import generate_embeddings, inference

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/generate_embeddings/{filepath:path}/{embedding_name}")
def generate_embed(filepath,embedding_name: str):
    generate_embeddings(pdf_filepath=filepath, embedding_name=embedding_name)
    
@app.get("/api/inference/{question}")
def run_inference(question, names: List[str] = Query(...)):
    return {
        "output": inference(question=question, embedding_names=names)
    }
    