# Gradio Chatbot using OpenAI's GPT-4 and Langchain, using Shiny for Python Documentation

This Python application provides a chatbot using OpenAI's GPT-4 model through the Langchain library. It utilizes Gradio for the user interface, allowing for interactive conversations. The chatbot uses the documentation for Shiny for Python as its knowledge base.

## How it Works

There are two main scripts in this application: `fetch_shiny_docs.py` and `chatbot.py`.

`fetch_shiny_docs.py` is responsible for pulling down the Shiny for Python documentation from the official GitHub repository. This documentation, stored in `.qmd` files, is cleaned, converted to `.txt` format, and saved into the `data` subfolder in the application's root directory.

`chatbot.py` is a question-answering bot that utilizes the documentation pulled by `fetch_shiny_docs.py` as its knowledge source. It starts by loading and preparing the textual data, creating embeddings that represent the meaning of the chunks of text from the documents. These embeddings are saved in a `.db` subfolder. Using these embeddings, the application can answer questions and carry out a conversation by finding the most relevant chunks to the current query.

## Embeddings and the `.db` Subfolder

This application will automatically look for a `.db` subfolder in the directory where `chatbot.py` is run. If found, it will load the precomputed embeddings from this directory, speeding up the startup process. If the `.db` subfolder does not exist, the application will create the embeddings from the text documents and save them in this subfolder for future use.

If you want to use different `.txt` files as your source documents, you will need to delete the existing `.db` subfolder before running `chatbot.py`. Alternatively, you can modify the `chatbot.py` script to point to a different directory for storing and loading embeddings.

## Required Input

You need to have an OpenAI API key for this to work.

If you would like to pull in new changes from the official repository, you can run `fetch_shiny_docs.py` yourself - otherwise, you can just run the chatbot. 

## How to Run

1. Ensure that you have installed all required Python libraries as listed in the `requirements.txt` file.

2. Set up your OpenAI API key. You need to store your API key in a text file located at `../key/key.txt`.

3. Run the `chatbot.py` Python script.

4. Wait for the Gradio interface to launch.

5. Start chatting with the bot!

## Ongoing Issues/Things to Keep In Mind

1. Unlike with the OpenAI GUI (https://chat.openai.com/), you are being charged by the token (word) that you submit to the API. You can track your costs/usage here. https://platform.openai.com/account/usage
2. This is not fast, and it's also going to take longer to run (and be more expensive) the longer the conversations are, so think about clearing the conversation and starting over if you don't need the context.
3. You can swap out different engines for either the embeddings or the LLM (like, if you want to use GPT-3.5).
4. You can swap out the Shiny .txt files with any other text files. If you want to use PDFs or other file types, you'll need to add those document processing functions from langchain. 
5. If you want to re-run the fetch_shiny_docs script, you'll need a GitHub API key called "github_token.txt" in your "keys" subfolder.
