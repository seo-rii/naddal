from langchain_core.runnables import RunnableLambda, RunnablePassthrough, Runnable
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter

class MyconversationChain(Runnable):
    def __init__(self, llm, prompt, memory, question_key='question', example_key='icl_examples', context_key='context'):
        self.prompt = prompt
        self.memory = memory
        self.question_key = question_key
        self.example_key = example_key
        self.context_key = context_key
        self.chain = (
            RunnablePassthrough.assign(
                chat_history=RunnableLambda(memory.load_memory_variables)
                | itemgetter(memory.memory_key)
                )
            | prompt
            | llm
            | StrOutputParser()
    )
    
    def invoke(self, query, sample=None, context=None, configs=None, **kwargs):
        answer = self.chain.invoke({self.question_key: query, self.example_key: sample, self.context_key: context})
        self.memory.save_context(inputs={'human':query}, outputs={'ai':answer})

        return answer