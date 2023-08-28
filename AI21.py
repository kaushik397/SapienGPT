import ai21
from langchain.llms import AI21
from langchain import PromptTemplate, LLMChain
from log import log
from audio import audio
#api_key = 'xgd3NNkjfM9IZpUoNrtA8Rr5V47zNg3W'
# https://sapiengpt-kaushi397.b4a.run/
def LLM(question,apikey,status):
    if apikey !='':
        log('we got API key',status=status)#prform the action 
        template = """
        Make a sales pitch of RedGear new computer mouse which is the best in the industry to {name} as they showed intrest in the product through website.
        """
        try:
            prompt = PromptTemplate(template=template, input_variables=["name"])
            llm = AI21(ai21_api_key=apikey)
            llm_chain = LLMChain(prompt=prompt, llm=llm)
            response = llm_chain.run(question)
            audio(response)
            return response
        except:
            return "provide valid APIkey"
    else:
        return "Please provide APIkey for AI21"