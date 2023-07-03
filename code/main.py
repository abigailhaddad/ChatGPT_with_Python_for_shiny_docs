# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 10:34:00 2023

@author: abiga
"""

import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
import gradio as gr
import pickle
import openai

def load_api_key(path):
    with open(path, "r") as key_file:
        return key_file.read().strip()

def initialize_chat_model(api_key_path, model_name="gpt-4", temperature=0):
    api_key = load_api_key(api_key_path)
    os.environ["OPENAI_API_KEY"] = api_key
    return ChatOpenAI(temperature=temperature, model_name=model_name)

def load_documents(loader_list, glob_pattern):
    documents = []
    for loader in loader_list:
        documents.extend(loader.load())
    return documents

def create_embeddings(documents, chunk_size=1000, chunk_overlap=0):
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    documents = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(documents, embeddings)
    return vectorstore

def initialize_qa_chain(llm, vectorstore):
    return ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever())

def launch_demo(qa_chain):
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot()
        msg = gr.Textbox()
        clear = gr.Button("Clear")
        def user(user_message, history):
            response = qa_chain({"question": user_message, "chat_history": history})
            history.append((user_message, response["answer"]))
            return gr.update(value=""), history

        msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False)
        clear.click(lambda: None, None, chatbot, queue=False)
    demo.launch(debug=True)

def main():
    glob_pattern = "**/*.txt"
    loader_list = [DirectoryLoader('../data/', glob_pattern)]
    llm = initialize_chat_model("../key/key.txt")

    # Load documents if not already done
    documents_path = "../data/documents.pkl"
    if os.path.exists(documents_path):
        with open(documents_path, "rb") as f:
            documents = pickle.load(f)
    else:
        documents = load_documents(loader_list, glob_pattern)
        with open(documents_path, "wb") as f:
            pickle.dump(documents, f)

    # Create embeddings if not already done
    embeddings_path = "../data/embeddings.pkl"
    if os.path.exists(embeddings_path):
        with open(embeddings_path, "rb") as f:
            vectorstore = pickle.load(f)
    else:
        vectorstore = create_embeddings(documents)
        with open(embeddings_path, "wb") as f:
            pickle.dump(vectorstore, f)

    qa_chain = initialize_qa_chain(llm, vectorstore)
    launch_demo(qa_chain)

if __name__ == "__main__":
    main()

