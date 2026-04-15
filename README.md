# advanced-rag-example
Sample Advanced RAG to query markdown documents.

## Installing dependencies
Install `uv` and execute the command `uv sync` in the project root to install dependencies.

## Setting up your environment variables
Create an .env file in the project root with your OpenAI and HuggingFace secret tokens
```
OPENAI_API_KEY=***
HF_TOKEN=***
```

## Ingesting markdown Ruby on Rails documentation in rorkb directory
To ingest the markdown files and convert them to a vector (Chroma) database run:
```
python withlangchain/ingest.py
```

## Running the Gradio interface
To run the chatbot UI (Gradio) run after having executed the ingestion:
```
python langchain_rag_app.py
```
