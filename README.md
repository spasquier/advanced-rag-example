# advanced-rag-example
Sample Advanced RAG to query markdown documents.

### Installing dependencies
Install `uv` and execute the command `uv sync` in the project root to install dependencies.

### Setting up your environment variables
Create an .env file in the project root with your OpenAI and HuggingFace secret tokens
```
OPENAI_API_KEY=***
HF_TOKEN=***
```
## Option A: RAG with Langchain

### Ingesting markdown Ruby on Rails documentation in rorkb directory
To ingest the markdown files and convert them to a vector (Chroma) database run:
```bash
python withlangchain/ingest.py
```

### Running the Gradio interface
To run the chatbot UI (Gradio) run after having executed the ingestion:
```bash
python langchain_rag_app.py
```
## Option B: RAG without Langchain

### Ingesting markdown Ruby on Rails documentation in rorkb directory
To ingest the markdown files without using the Langchain:
```bash
python advanced/ingest.py
```

### Running the Gradio interface
To run the chatbot UI (Gradio) after having executed the advanced ingestion without Langchain:
```bash
python advanced_rag_app.py
```
