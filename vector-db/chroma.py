import os
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from dotenv import load_dotenv

load_dotenv()

directory = "./vector-db/descriptions"
docs = []
client = chromadb.PersistentClient(path="./vector-db/vectorstore")
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.getenv("OPENAI_API_KEY"),
            )
collection = client.get_or_create_collection(name="my_collection", embedding_function=openai_ef)

# Load JSON files from descriptions directory
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            data = json.load(file)
            link = data.get("link")
            description_data = json.loads(data.get("description", "{}"))
            title = description_data.get("title", "Untitled")
            actions = description_data.get("actions", [])
            
            # Join actions into a single text for chunking if necessary
            description_text = " ".join(actions)
            
            # Create a Document with the content and metadata
            doc = Document(page_content=description_text, metadata={"link": link, "title": title, "filename": filename})
            docs.append(doc)

# Split documents into chunks if larger than 500 characters
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)
all_splits = text_splitter.split_documents(docs)

# Prepare documents, metadata, and IDs for adding to the collection
documents = [doc.page_content for doc in all_splits]
metadatas = [doc.metadata for doc in all_splits]
ids = [f"doc_{i}" for i in range(len(all_splits))]

# Add documents to the Chroma collection
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)
print("Documents processed and stored in Chroma vector database.")
