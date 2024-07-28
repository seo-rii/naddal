import base64
import os
from typing import Union, List

from langchain_community.document_loaders import ArxivLoader
import requests

from dotenv import load_dotenv
import oracledb
from utils import inference
from paper_handler import chat, get_paper_list
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from paper_handler import upload_pdf, get_paper_by_id
from chat_handler import get_chat_list
from type import ChatRequest, PDFRequest, MarkRequest, PaperPatchRequest, TranslationApi

from fastapi.responses import FileResponse
import json
from translation import translation

from pinecone import Pinecone


# from utils import reembed_paper # reembed_paper 함수 가져오기

app = FastAPI()
load_dotenv(".env")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("UPSTAGE_API_KEY")
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))


@app.get("/")
def read_root():
    return {"data": {"Hello": "World"}}


@app.get("/api/inference/{question}")
def run_inference(question, names: List[str] = Query(...)):
    return {"data": {"output": inference(question=question, embedding_names=names)}}


@app.get("/api/paper")
def get_paper():
    return {"data": {"list": get_paper_list()}}


@app.get("/api/paper/{paper_id}")
def get_paper(paper_id: str):
    try:
        paper_id = int(paper_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Paper ID must be an integer")
    result = get_paper_by_id(paper_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    result["author"] = "Unknown"
    result["abstract"] = "Unknown"
    return {"data": result}


@app.post("/api/paper")
def post_paper(pdf_request: PDFRequest):
    try:
        result = upload_pdf(pdf_request, pc)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/api/arxiv/{paper_id}")
def post_arxiv_paper(paper_id: str):
    try:
        loader = ArxivLoader(
            query=paper_id,
            load_max_docs=1,
            load_all_available_meta=True,
        )
        docs = loader.load()
        url = docs[0].metadata['links'][1]
        pdfFile = requests.get(url, allow_redirects=True).content
        # name, pdffile base64 encode
        pdf_request = PDFRequest(file_name=paper_id, file_data=base64.b64encode(pdfFile))
        result = upload_pdf(pdf_request, pc)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/api/paper/{paper_id}")
def patch_paper(paper_id: int, paper_patch_request: PaperPatchRequest):
    try:
        paper = get_paper_by_id(paper_id)
        if paper is None:
            raise HTTPException(status_code=404, detail="Paper not found")

        file_path = f"./uploads/{paper['title']}_{paper_id}/parsed.html"
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        with open(file_path, "w") as f:
            f.write(paper_patch_request.raw)
            
        # reembed_paper(paper_patch_request.raw, str(paper_id), pc) # JHJ
        
        return {"data": "success"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/chat")
def get_chat():
    return {"data": get_chat_list()}


@app.get("/api/chat/{chat_id}")
def get_chat_history(chat_id: int):
    chat_path = f"./chat/{chat_id}/chat.json"
    if not os.path.exists(chat_path):
        raise HTTPException(status_code=404, detail="Chat not found")
    with open(chat_path, "r") as f:
        chat_log = json.load(f)
        return {"data": chat_log}


@app.post("/api/chat")
def post_chat(chat_request: ChatRequest):
    try:
        result = chat(chat_request=chat_request)
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/image/{paper_id}/{image_name}")
def get_image(paper_id: int, image_name: str):
    result = get_paper_by_id(paper_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    image_path = f"./uploads/{result['title']}_{paper_id}/{image_name}"
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path)


@app.get("/api/mark/{paper_id}")
def get_mark(paper_id: int):
    mark_path = f"./mark/{paper_id}.json"
    if not os.path.exists(mark_path):
        return []
    with open(mark_path, "r") as f:
        st = f.read()
        js = json.loads(st)
        return js


@app.get("/api/mark")
def get_all_mark():
    mark_list = []
    for file in os.listdir("./mark"):
        if file.startswith("."):
            continue
        with open(f"./mark/{file}", "r") as f:
            st = f.read()
            js = json.loads(st)
            mark_list += js
    return {"data": {"list": mark_list}}


@app.post("/api/mark/{paper_id}")
def post_mark(paper_id: int, mark_request: MarkRequest):
    if not os.path.exists("./mark"):
        os.makedirs("./mark")
    mark = mark_request.marks
    mark_path = f"./mark/{paper_id}.json"
    with open(mark_path, "w") as f:
        f.write(json.dumps(mark))
    return {"data": "success"}


@app.post("/api/translation")
def post_translation(translation_api: TranslationApi):
    try:
        result = translation(translation_api.raw)
        return {"data": {"raw": result}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
