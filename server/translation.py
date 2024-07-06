from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


def translation(text):

    enko_translation = ChatUpstage(model="solar-1-mini-translate-enko")

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{text}"),
        ]
    )

    chain = chat_prompt | enko_translation | StrOutputParser()
    return chain.invoke({"text": text})
