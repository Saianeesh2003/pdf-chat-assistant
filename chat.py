from dotenv import load_dotenv
from google import genai
from google.genai import types
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore 

load_dotenv()
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

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
    
    SYSTEM_PROMPT = f"""
    You are a helpful AI Assistant who answers user queries based on the available context
    retrieved from a PDF file along with page contents and page numbers.

    You should only answer the user based on the following context and navigate the user
    to open the right page number to know more.
    Also if there is any topic which might require a code as sample example you can give it as well.
    Also if in case user asks to give me a summary of entire PDF you can do it.
    
    Context:
    {context}
    """
    
    contents = [
        {"role": "user", "parts": [{"text": query}]} 
    ]
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.7,
        )
    )
    
    print(f"\n🤖 {response.text}\n")