import streamlit as st
from dotenv import load_dotenv
from anthropic import Anthropic
import os
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore

# Qdrant configuration - works for both local and cloud
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)

# Page config
st.set_page_config(
    page_title="PDF Chat Assistant",
    page_icon="📚",
    layout="wide"
)

# Load environment variables
load_dotenv()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'vector_db' not in st.session_state:
    st.session_state.vector_db = None
if 'indexed' not in st.session_state:
    st.session_state.indexed = False

# Initialize clients
@st.cache_resource
def init_clients():
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    return client, embeddings

client, embeddings = init_clients()

# Sidebar for PDF upload and indexing
with st.sidebar:
    st.title("📚 PDF Chat Assistant")
    st.markdown("*Powered by Claude*")
    st.markdown("---")
    
    # PDF Upload
    uploaded_file = st.file_uploader("Upload a PDF", type=['pdf'])
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        pdf_path = Path("temp_uploaded.pdf")
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if st.button("🔄 Index PDF", type="primary"):
            with st.spinner("Indexing PDF... This may take a moment."):
                try:
                    # Load PDF
                    loader = PyPDFLoader(str(pdf_path))
                    docs = loader.load()
                    
                    # Chunk documents
                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=400
                    )
                    splited_docs = text_splitter.split_documents(documents=docs)
                    
                    # Create vector store
                    collection_name = f"pdf_docs_{uploaded_file.name.replace('.pdf', '')}"
                    vectorstore = QdrantVectorStore.from_documents(
                        documents=splited_docs,
                        embedding=embeddings,
                        collection_name=collection_name,
                        url=QDRANT_URL,
                        api_key=QDRANT_API_KEY
                    )
                    
                    st.session_state.vector_db = vectorstore
                    st.session_state.indexed = True
                    st.session_state.collection_name = collection_name
                    
                    st.success(f"✅ Indexed {len(splited_docs)} chunks successfully!")
                except Exception as e:
                    st.error(f"Error indexing PDF: {str(e)}")
    
    # Option to load existing collection
    st.markdown("---")
    st.subheader("Or Load Existing Collection")
    collection_name_input = st.text_input("Collection Name", value="nodejs_docs")
    
    if st.button("📂 Load Collection"):
        try:
            vector_db = QdrantVectorStore.from_existing_collection(
                embedding=embeddings,
                collection_name=collection_name_input,
                url=QDRANT_URL,
                api_key=QDRANT_API_KEY
            )
            st.session_state.vector_db = vector_db
            st.session_state.indexed = True
            st.session_state.collection_name = collection_name_input
            st.success(f"✅ Loaded collection: {collection_name_input}")
        except Exception as e:
            st.error(f"Error loading collection: {str(e)}")
    
    # Display status
    st.markdown("---")
    if st.session_state.indexed:
        st.success("🟢 Ready to chat!")
        st.info(f"Collection: {st.session_state.get('collection_name', 'N/A')}")
    else:
        st.warning("⚠️ Please index a PDF or load a collection first")
    
    # Settings - collapsed by default
    st.markdown("---")
    with st.expander("⚙️ Settings", expanded=False):
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
        num_results = st.slider("Number of context chunks", 1, 5, 3)
        max_tokens = st.slider("Max tokens", 500, 4000, 2000, 100)

# Main chat interface
st.title("💬 Chat with Your PDF")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("📄 View Sources"):
                st.markdown(message["sources"])

# Chat input
if prompt := st.chat_input("Ask a question about your PDF..."):
    if not st.session_state.indexed:
        st.error("Please index a PDF or load a collection first!")
    else:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Search for relevant chunks
                    search_results = st.session_state.vector_db.similarity_search(
                        query=prompt, 
                        k=num_results
                    )
                    
                    # Build context
                    context = "\n\n".join([
                        f"Page Content: {result.page_content}\nPage Number: {result.metadata.get('page', 'N/A')}"
                        for result in search_results
                    ])
                    
                    # Build sources display
                    sources_text = ""
                    for i, result in enumerate(search_results, 1):
                        sources_text += f"**Source {i}** (Page {result.metadata.get('page', 'N/A')}):\n"
                        sources_text += f"{result.page_content[:200]}...\n\n"
                    
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
                        model="claude-sonnet-4-20250514",
                        max_tokens=max_tokens,
                        system=SYSTEM_PROMPT,
                        messages=[
                            {
                                "role": "user",
                                "content": f"Context:\n{context}\n\nQuestion: {prompt}"
                            }
                        ],
                        temperature=temperature
                    )
                    
                    response_text = response.content[0].text
                    st.markdown(response_text)
                    
                    # Show sources
                    with st.expander("📄 View Sources"):
                        st.markdown(sources_text)
                    
                    # Add assistant response to chat
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response_text,
                        "sources": sources_text
                    })
                    
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")

# Clear chat button
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.rerun()