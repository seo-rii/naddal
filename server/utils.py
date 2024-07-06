import os
from dotenv import load_dotenv, find_dotenv
from langchain_chroma import Chroma
from langchain_upstage import UpstageEmbeddings
from langchain_upstage import UpstageLayoutAnalysisLoader
from langchain.docstore.document import Document
from langchain_upstage import ChatUpstage
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
import re


def tag_remover(html_content: str) -> str:
    """Remove html tags and extract only contents"""
    tag_regex = r"<[^>]*>"
    return re.sub(tag_regex, "", html_content)


def pdf_to_html(pdf_filepath):
    layzer = UpstageLayoutAnalysisLoader(pdf_filepath, output_type="html")
    docs = layzer.load()
    return docs


# generate function for generate embedding
def generate_embeddings(pdf_filepath, embedding_name):
    """
    Generate Embeddings for the given pdf, return 1 if success otherwise return 0
    """
    load_dotenv(find_dotenv())
    api_key = os.getenv("UPSTAGE_API_KEY")
    try:
        layzer = UpstageLayoutAnalysisLoader(pdf_filepath, output_type="html")
        docs = layzer.load()
        # split text into text chunks
        text_spliiter = RecursiveCharacterTextSplitter.from_language(
            chunk_size=1000, chunk_overlap=100, language=Language.HTML
        )
        splits = text_spliiter.split_documents(docs)
        splits = [tag_remover(split.page_content) for split in splits]
        unique_splits = []
        for split in splits:
            if split not in unique_splits:
                unique_splits.append(split)
        persist_directory = f"./chroma_db/{embedding_name}/"
        vectorstore = Chroma.from_documents(
            documents=unique_splits,
            ids=[doc.page_content for doc in unique_splits],
            embedding=UpstageEmbeddings(
                model="solar-embedding-1-large", api_key=api_key
            ),
            persist_directory=persist_directory,
        )
        print(f"embedding saved in ./chroma_db/{embedding_name}/")
        return 1
    except Exception as e:
        print(e)
        return 0


def inference(question, embedding_names):
    """
    run inference for a given question and use retriver based on the given embedding_names
    ## params
    - question (str): user query
    - embedding_names (List[str]): embedding names that the retriever should use it
    """
    load_dotenv(find_dotenv())
    api_key = os.getenv("UPSTAGE_API_KEY")

    def retrieve(retriever, input_query):
        return retriever.invoke(input_query)

    def get_retriever(embedding_name):
        return Chroma(
            persist_directory=f"./chroma_db/{embedding_name}/",
            embedding_function=UpstageEmbeddings(model="solar-embedding-1-large"),
        ).as_retriever()

    name_list = os.listdir("./chroma_db/")
    embedding_names = list(set(embedding_names))
    # check if their are any invalid names of embeddings
    print("[[CHECKING EMBEDDING NAMES...]]")
    for name in embedding_names:
        if name not in embedding_names:
            raise Exception(f"{name} embedding not found.")

    print("[[LOADING EMBEDDINGS...]]")
    # accumulate retrivers into a single list
    retrievers = []
    for name in embedding_names:
        retriever = get_retriever(name)
        print(retriever)
        retrievers.append((retriever, name))
    # generate documents
    print("[[RETRIEVING RELEVANT DOCS...]]")
    context = ""
    for retriever in retrievers:
        result = retrieve(retriever[0], question)
        print(result)
        # TODO post process result
        # - html 정제하기
        # - 순수 text 뽑기
        refined_result = "" + f"from [{retriever[1]}]"
        context += refined_result + "\n\n"

    system_msg = SystemMessagePromptTemplate.from_template(
        "You are an assistant for question-answering tasks.\n"
        "Use the following pieces of retrieved context to answer the question.\n"
        "If you don't know the answer, just say that you don't know.\n"
        "Also, when giving an output, please give the reference for each sentence.\n"
        "In total, strictly follow the format below for each sentences:\n"
        "output sentence(reference name which is mentioned in the context)"
        "Use three sentences maximum and keep the answer concise.\n"
    )
    human_msg = HumanMessagePromptTemplate.from_template(
        "Question: {question}\n\n" "Context: {context}" "Answer:"
    )
    chat_prompt = ChatPromptTemplate.from_messages([system_msg, human_msg])
    model = ChatUpstage(api_key=api_key)
    chain = chat_prompt | model
    output = chain.invoke({"question": question, "context": context})
    return output.content
