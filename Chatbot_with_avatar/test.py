import pickle
from langchain_helper import create_pickle_file

create_pickle_file()

fileObj = open("data.obj", "rb")
chat = pickle.load(fileObj)
fileObj.close()

# answer = chat.return_response("Who is the ceo of Tesla")
answer = chat.return_response("can you tell me about ivy")
print(answer)
print(chat.chat_history)


# fileObj = open('data.obj', 'wb')
# pickle.dump(chat,fileObj)
# fileObj.close()
