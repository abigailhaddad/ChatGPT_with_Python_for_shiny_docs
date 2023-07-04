import gradio as gr
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
import chromadb
import os

def load_api_key(path):
    with open(path, "r") as key_file:
        return key_file.read().strip()

def initialize_chat_model(api_key_path, model_name="gpt-4", temperature=0):
    api_key = load_api_key(api_key_path)
    os.environ["OPENAI_API_KEY"] = api_key
    return ChatOpenAI(temperature=temperature, model_name=model_name, openai_api_key=api_key)

def load_documents(glob_pattern):
    txt_loader = DirectoryLoader('../data/', glob=glob_pattern)
    documents = txt_loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(documents)
    return documents

def create_or_load_chroma_collection(collection_name="my_collection"):
    chroma_client = chromadb.Client()
    collection = chroma_client.get_collection(collection_name)

    # If collection doesn't exist, create a new one
    if not collection:
        collection = chroma_client.create_collection(name=collection_name)

    return collection, chroma_client

def add_documents_to_collection(collection, documents):
    collection.add(
        documents=documents,
        metadatas=[{"source": "my_source"}] * len(documents),
        ids=[str(i) for i in range(len(documents))]
    )

def initialize_chroma_vectorstore(documents, collection_name="my_collection"):
    collection, chroma_client = create_or_load_chroma_collection(collection_name)

    # If the collection is empty, add documents
    if collection.count() == 0:
        add_documents_to_collection(collection, documents)

    return collection, chroma_client

def initialize_qa_chain(llm, vectorstore):
    return ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever())

def launch_demo(qa_chain):
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot()
        msg = gr.Textbox()
        clear = gr.Button("Clear")

        def user(user_message, history=[]):
            # Format chat history
            formatted_chat_history = []
            for h in history:
                user_msg = ("user", h[0])
                assistant_msg = ("assistant", h[1])
                formatted_chat_history.append(user_msg)
                formatted_chat_history.append(assistant_msg)

            # Generate response using QA chain
            response = qa_chain({"question": user_message, "chat_history": formatted_chat_history})

            # Append user message and response to chat history
            new_history = history + [(user_message, response["answer"])]

            return gr.update(value=""), new_history

        msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False)
        clear.click(lambda: None, None, chatbot, queue=False)
    demo.launch(debug=True)

def main():
    glob_pattern = "**/*.txt"
    llm = initialize_chat_model("../key/key.txt")

    # Load documents
    documents = load_documents(glob_pattern)
    print("loaded_documents")

    # Create or load Chroma vectorstore
    vectorstore, chroma_client = initialize_chroma_vectorstore(documents)
    print("created or loaded vectorstore")

    qa_chain = initialize_qa_chain(llm, vectorstore)
    print("initialized qa_chain")

    launch_demo(qa_chain)

    # Close the Chroma client
    chroma_client.close()

if __name__ == "__main__":
    main()
