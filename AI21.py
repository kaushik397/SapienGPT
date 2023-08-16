import ai21
from langchain.llms import AI21
from langchain import PromptTemplate, LLMChain
from log import log
#api_key = 'xgd3NNkjfM9IZpUoNrtA8Rr5V47zNg3W'

def LLM(question,apikey,status):
    if apikey !='':
        log('we got API key',status=status)#prform the action 
        template = """
        Explain {question} as a teacher"""
        try:
            prompt = PromptTemplate(template=template, input_variables=["question"])
            llm = AI21(ai21_api_key=apikey)
            llm_chain = LLMChain(prompt=prompt, llm=llm)
            return llm_chain.run(question)
        except:
            return "provide valid API key"
    else:
        return "Please provide APIkey for AI21"