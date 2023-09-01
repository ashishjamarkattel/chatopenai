## setup a mongodb client
uri = "mongodb+srv://ashish:test@cluster0.sabimdx.mongodb.net/?retryWrites=true&w=majority"
##connect mongodb client to langchain
message_history = MongoDBChatMessageHistory(
        connection_string=uri, session_id= "abc"
    )
##setup buffermemory 
memory = ConversationBufferMemory()
##add message history from mongodb to buffermemory
memories.save_context(
                    {"input": message_history.messages[0].content}, 
                    {"output": message_history.messages[1].content}
                    )
##connect llm, buffermemory to langchain
os.environ["OPENAI_API_KEY"] = ""
llm = OpenAI(temperature=0.5)
conversation = ConversationChain(
                                llm=llm,
                                verbose=False,
                                prompt = PROMPT,
                                memory=memories 
                                )
## get the result
conv = conversation.predict(input= "what is your name?", link= ""abc"")