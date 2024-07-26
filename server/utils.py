import os
from typing import List
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

from ground_checker import pass_answer
from smart_rag import smart_rag

import oracledb
from langchain_community.vectorstores.oraclevs import OracleVS
from langchain_community.vectorstores.utils import DistanceStrategy


def tag_remover(html_content: str) -> str:
    """Remove html tags and extract only contents"""
    tag_regex = r"<[^>]*>"
    return re.sub(tag_regex, "", html_content)


def pdf_to_html(pdf_filepath):
    layzer = UpstageLayoutAnalysisLoader(pdf_filepath, output_type="html")
    docs = layzer.load()
    return docs


icl_examples = """
Question: What is attention mechanism and how is it used in bert and gpt?
Context: Fine-tuning is straightforward since the self-attention mechanism in the Transformer al-lows BERT to model many downstream tasks—whether they involve single text or text pairs—byswapping out the appropriate inputs and outputs.For applications involving text pairs, a commonpattern is to independently encode text pairs be-fore applying bidirectional cross attention, suchas Parikh et al. ( 2016 ); Seo et al. ( 2017 ). BERTinstead uses the self-attention mechanism to unifythese two stages, as encoding a concatenated textpair with self-attention effectively includes bidi-rectional cross attention between two sentences. from [bert, page number: 5]

Dehghani, M., Gouws, S., Vinyals, O., Uszkoreit, J., and Kaiser,Ł . Universal transformers. arXiv preprint arXiv:1807.03819 ,2018. Devlin, J., Chang, M.-W., Lee, K., and Toutanova, K. Bert: Pre-training of deep bidirectional transformers for language under-standing. arXiv preprint arXiv:1810.04805 , 2018. Dinan, E., Roller, S., Shuster, K., Fan, A., Auli, M., and Weston,J. Wizard of wikipedia: Knowledge-powered conversationalagents. arXiv preprint arXiv:1811.01241 , 2018. Fan, A., Lewis, M., and Dauphin, Y. Hierarchical neural storygeneration. arXiv preprint arXiv:1805.04833 , 2018.from [gpt, page number: 10]

Attention mechanisms have become an integral part of compelling sequence modeling and transduc-tion models in various tasks, allowing modeling of dependencies without regard to their distance inthe input or output sequences [ 2 , 19 ]. In all but a few cases [ 27 ], however, such attention mechanismsare used in conjunction with a recurrent network. In this work we propose the Transformer, a model architecture eschewing recurrence and insteadrelying entirely on an attention mechanism to draw global dependencies between input and output.The Transformer allows for significantly more parallelization and can reach a new state of the art intranslation quality after being trained for as little as twelve hours on eight P100 GPUs. 2 Backgroundfrom [attention, page number: 2]

Answer:
Attention mechanism is an integral part of powerful sequence modeling and transduction models in various tasks, allowing modeling of dependencies without regard to their distance in the input or output sequences [1]. In this work, the Transformer model architecture is proposed, which relies entirely on an attention mechanism to draw global dependencies between input and output, allowing for significant parallelization and achieving a new state of the art in translation quality (1).
In the context of BERT, the self-attention mechanism allows for fine-tuning and modeling of many downstream tasks by swapping out the appropriate inputs and outputs [2]. BERT unifies encoding and bidirectional cross attention between two sentences using the self-attention mechanism (2).
In the context of GPT, fine-tuning is straightforward since the self-attention mechanism in the Transformer allows for modeling of many downstream tasks involving text pairs by independently encoding text pairs before applying bidirectional cross attention (3).

References
(1) attention (page number: 2)
(2) bert (page number: 5)
(3) gpt (page number: 10)
"""


# generate function for generate embedding
def generate_embeddings(docs: List[Document], embedding_name, client):
    """
    Generate Embeddings for the given pdf, return 1 if success otherwise return 0
    """
    # split text into text chunks
    text_spliiter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    # text_spliiter = RecursiveCharacterTextSplitter.from_language(
    #     chunk_size=1000, chunk_overlap=100, language=Language.HTML
    # )
    splits = text_spliiter.split_documents(docs)
    for split in splits:
        split.page_content = tag_remover(split.page_content)
    unique_splits = []
    for split in splits:
        if split not in unique_splits and split.page_content != "":
            unique_splits.append(split)

    knowledge_base = OracleVS.from_documents(
        unique_splits,
        UpstageEmbeddings(
            model="solar-embedding-1-large", api_key=os.environ["UPSTAGE_API_KEY"]
        ),
        client=client,
        table_name=f"id{embedding_name}",
        distance_strategy=DistanceStrategy.DOT_PRODUCT,
    )

    print(
        f"""embedding saved in oracledb \n
                table name: id{embedding_name}"""
    )

    return knowledge_base


def inference(question, embedding_names):
    """
    run inference for a given question and use retriver based on the given embedding_names
    ## params
    - question (str): user query
    - embedding_names (List[str]): embedding names that the retriever should use it
    """
    load_dotenv(find_dotenv())
    api_key = os.getenv("UPSTAGE_API_KEY")

    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    dsn = os.getenv("DSN")

    try:
        conn23c = oracledb.connect(user=username, password=password, dsn=dsn)
        print("Connection successful!", conn23c.version)
    except Exception as e:
        print("Connection failed!")

    def retrieve(retriever, input_query):
        return retriever.invoke(input_query)

    def get_retriever(embedding_name):
        return OracleVS(
            client=conn23c,
            embedding_function=UpstageEmbeddings(model="solar-embedding-1-large"),
            table_name=f"{embedding_name}",
            distance_strategy=DistanceStrategy.DOT_PRODUCT,
        ).as_retriever()

    print("[[LOADING EMBEDDINGS...]]")
    # accumulate retrivers into a single list
    retrievers = []
    for name in embedding_names:
        retriever = get_retriever(name)
        # print(retriever)
        retrievers.append((retriever, name))
    # generate documents
    print(retrievers)
    print("[[RETRIEVING RELEVANT DOCS...]]")
    context = ""
    for retriever in retrievers:
        result = retrieve(retriever[0], question)

        result = [(r.page_content, r.metadata) for r in result]

        print(result)

        for idx in range(min(2, len(result))):
            refined_result = (
                result[idx][0]
                + f"from [{retriever[1]}, page number: {result[idx][1]['page']}]"
            )
            context += refined_result + "\n\n"
    print(f"context: {context}\n\n")

    system_msg = SystemMessagePromptTemplate.from_template(
        "You are a helpful assistant."
    )
    human_msg = HumanMessagePromptTemplate.from_template(
        "You are an assistant for question-answering tasks.\n"
        "Use the following pieces of retrieved context to answer the question.\n"
        "If you don't know the answer, just say that you don't know.\n"
        "Also, when giving an output, please give the reference for each sentence.\n"
        "In total, strictly follow the rules for formatting the output below:\n"
        "1. If the sentence is cited from the given context, end up the sentence with a \"reference number\" that indicates the reference like ['numerical value'].\n"
        "2. The number at the end of sentence will indicate the reference below, which is consist of reference number, reference name, and page number."
        "3. You don't need to put a reference for every sentence, but it is important to put reference if needed."
        "4. Generate an output sentence that is only based on the given context.\n"
        "Here is an icl example:\n\n"
        "{icl_examples}\n\n"
        "Now begin!\n"
        "Question: {question}\n\n"
        "Context: {context}"
        "[Output start]\n"
    )
    chat_prompt = ChatPromptTemplate.from_messages([system_msg, human_msg])
    model = ChatUpstage(api_key=api_key)
    chain = chat_prompt | model
    truth, output = pass_answer(3, chain, icl_examples, question, context)
    if not truth:
        return (
            "Sorry, we cannot find the related information. But we search about that. \n"
            + smart_rag(chain, question, context)
        )
    return output
