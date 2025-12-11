from dotenv import load_dotenv
from anthropic import Anthropic
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore 

load_dotenv()

# Initialize Claude client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Keep using Google embeddings (they work great!)
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004"
)

# Use environment variables for security
vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name="nodejs_docs",
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

print("💬 Chat with your PDF (type 'exit' to quit)\n")

while True:
    query = input("> ")
    if query.lower() in ['exit', 'quit', 'q']:
        print("Goodbye! 👋")
        break
    
    search_results = vector_db.similarity_search(query=query, k=3)
    
    context = "\n\n".join([
        f"Page Content: {result.page_content}\nPage Number: {result.metadata.get('page', 'N/A')}"
        for result in search_results
    ])
    
    SYSTEM_PROMPT = """
    You are a helpful AI Assistant who answers user queries based on the available context
    retrieved from a PDF file along with page contents and page numbers.

    You should only answer the user based on the following context and navigate the user
    to open the right page number to know more.
    Also if there is any topic which might require a code as sample example you can give it as well.
    Also if in case user asks to give me a summary of entire PDF you can do it.
    """
    
    # Claude API call
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",  
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}"
            }
        ],
        temperature=0.7
    )
    
    print(f"\n🤖 {response.content[0].text}\n")