from dotenv import load_dotenv
from google import genai
from google.genai import types
import os
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore 

load_dotenv()
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

pdf_path = Path(__file__).parent / "nodejs.pdf"
loader = PyPDFLoader(pdf_path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)

splited_docs = text_splitter.split_documents(documents=docs)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004"
)

# Use environment variables for security
vectorstore = QdrantVectorStore.from_documents(
    documents=splited_docs,
    embedding=embeddings,
    collection_name="nodejs_docs",
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

print("Indexing of Documents Done...")