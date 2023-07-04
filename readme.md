# Gradio Chatbot using OpenAI's GPT-4 and Langchain

This Python application provides a chatbot using the OpenAI's GPT-4 model through the Langchain library. It utilizes Gradio for the user interface, allowing for interactive conversations.

## How it Works

The application starts by loading and preparing your textual data. This data is then used to create embeddings, which represent the meaning of the chunks of text from your documents. Using these embeddings, the application can answer questions and carry out a conversation by finding the most relevant chunks to the current query.

## Required Input

Currently, the chatbot is configured to process `.txt` files. However, it can be modified to process other file formats like `.pdf`, `.docx`, etc., by incorporating the respective document loaders from the Langchain library.

The input files should be placed in the `data` subfolder in the application's root directory.

## How to Run

1. Ensure that you have installed all required Python libraries as listed in the `requirements.txt` file.

2. Set up your OpenAI API key. You need to store your API key in a text file located at `../key/key.txt`.

3. Run the `main.py` Python script.

4. Wait for the Gradio interface to launch.

5. Start chatting with the bot!
