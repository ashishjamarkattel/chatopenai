from langchain.llms import OpenAI
from langchain.chains import ConversationChain
import os
from langchain.memory import ConversationBufferMemory
from typing import List,Dict, Any
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import MongoDBChatMessageHistory
from fastapi import FastAPI

##setup up mongodb client
uri = ""

##setup a openai
os.environ["OPENAI_API_KEY"] = ""
llm = OpenAI(temperature=0.5)

app = FastAPI(desc="Chatbot")

_DEFAULT_TEMPLATE = """you are the chatbot that is prepared by whispering ai
This is the history about the user
{history} and this is the recent conversation
{input}

"""

@app.post("/chat")
def chatbot(input, session):
    message_history = MongoDBChatMessageHistory(
        connection_string=uri, session_id= session
    )
    PROMPT = PromptTemplate(
                input_variables=["history","input"],
                template=_DEFAULT_TEMPLATE,
                )
    memories = ConversationBufferMemory(k=3)

    if len(message_history.messages):
        memories.save_context(
                                {"input": message_history.messages[0].content}, 
                                {"output": message_history.messages[1].content}
                                )
        conversation = ConversationChain(
                                            llm=llm,
                                            verbose=False,
                                            prompt = PROMPT,
                                            memory=memories 
                                            )
        conv = conversation.predict(input=input)
        message_history.add_user_message(input)
        message_history.add_ai_message(conv)
        return conv


    else:
        conversation = ConversationChain(
                                            llm=llm,
                                            verbose=False,
                                            prompt = PROMPT,
                                            memory=memories
                                            )
        conv = conversation.predict(input=input)
        message_history.add_user_message(input)
        message_history.add_ai_message(conv)
        return conv
