import os
from tavily import TavilyClient


def smart_rag(chain, question, context):

    print("Searching in tavily")
    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    context = tavily.search(query=question)

    return chain.invoke({"context": context, "question": question}).content
