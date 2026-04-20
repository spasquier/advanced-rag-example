# Imports and constants
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from chromadb import PersistentClient
from tqdm import tqdm

load_dotenv(override=True)

MODEL = "ollama/llama3.1:8b" # LiteLLM completion model
DB_NAME = "advanced_db"
KNOWLEDGE_BASE_PATH = Path("ror_kb")
AVERAGE_CHUNK_SIZE = 1100

COLLECTION_NAME = "docs"
EMBEDDING_MODEL = "nomic-embed-text-v2-moe"
ollama = OpenAI(base_url="http://localhost:11434/v1", api_key='ollama')

# LangChain's Document equivalent
class Result(BaseModel):
    page_content: str
    metadata: dict


# A class that represents a chunk
class Chunk(BaseModel):
    headline: str = Field(description="A brief heading for this chunk, typically a few words, that is most likely to be surfaced in a query")
    summary: str = Field(description="A few sentences summarizing the content of this chunk to answer common questions")
    original_text: str = Field(description="The original text of this chunk from the provided document, exactly as is, not changed in any way")

    def as_result(self, document):
        metadata = {"source": document["source"], "type": document["type"]}
        return Result(page_content=self.headline + "\n\n" + self.summary + "\n\n" + self.original_text,metadata=metadata)


class Chunks(BaseModel):
    chunks: list[Chunk]


def fetch_documents():
    """A homemade version of the LangChain DirectoryLoader"""

    documents = []

    for folder in KNOWLEDGE_BASE_PATH.iterdir():
        doc_type = folder.name
        for file in folder.rglob("*.md"):
            with open(file, "r", encoding="utf-8") as f:
                documents.append({"type": doc_type, "source": file.as_posix(), "text": f.read()})

    print(f"Loaded {len(documents)} documents")
    return documents


def process_document(document):
    # Deterministic chunking: split the document into overlapping
    # chunks of `chunk_size` characters with `overlap` characters overlap.
    text = document.get("text", "") or ""
    chunk_size = AVERAGE_CHUNK_SIZE
    overlap = 200
    step = chunk_size - overlap if chunk_size > overlap else chunk_size

    if not text:
        return []

    chunks = []
    start = 0
    text_len = len(text)
    import re

    while start < text_len:
        end = start + chunk_size
        chunk_text = text[start:end]

        # Headline: first non-empty line or a trimmed prefix
        stripped = chunk_text.strip()
        if stripped:
            first_line = stripped.splitlines()[0].strip()
            headline = (first_line[:75].rstrip() + "...") if len(first_line) > 75 else first_line
        else:
            headline = ""

        # Summary: prefer the first sentence; otherwise a trimmed prefix
        max_summary_len = 200
        m = re.search(r'([^.?!]*[.?!])', stripped)
        if m and len(m.group(0)) <= max_summary_len:
            summary = m.group(0).strip()
        else:
            summary = (stripped[:max_summary_len].rstrip() + "...") if len(stripped) > max_summary_len else stripped

        chunks.append(Chunk(headline=headline, summary=summary, original_text=chunk_text))

        start += step

        if end >= text_len:
            break

    return [chunk.as_result(document) for chunk in chunks]


def create_chunks(documents):
    chunks = []
    for doc in tqdm(documents):
        chunks.extend(process_document(doc))
    return chunks


def create_embeddings(chunks):
    chroma = PersistentClient(path=DB_NAME)
    if COLLECTION_NAME in [c.name for c in chroma.list_collections()]:
        chroma.delete_collection(COLLECTION_NAME)

    texts = [chunk.page_content for chunk in chunks]
    emb = ollama.embeddings.create(model=EMBEDDING_MODEL, input=texts).data
    vectors = [e.embedding for e in emb]

    collection = chroma.get_or_create_collection(COLLECTION_NAME)

    ids = [str(i) for i in range(len(chunks))]
    metas = [chunk.metadata for chunk in chunks]

    collection.add(ids=ids, embeddings=vectors, documents=texts, metadatas=metas)
    print(f"Vectorstore created with {collection.count()} documents")


if __name__ == "__main__":
    documents = fetch_documents()
    chunks = create_chunks(documents)
    create_embeddings(chunks)
    print("Ingestion complete")

