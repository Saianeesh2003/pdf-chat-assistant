# 📚 PDF Chat Assistant with RAG

An intelligent PDF chatbot powered by Retrieval Augmented Generation (RAG) that allows users to have natural conversations with their PDF documents. Built with Google Gemini, LangChain, and Qdrant vector database.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](your-app-url-here)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

- **📄 PDF Upload & Processing**: Upload any PDF document and chat with its content
- **🤖 AI-Powered Responses**: Leverages Google Gemini 2.0 for intelligent answers
- **🔍 Semantic Search**: Uses advanced vector embeddings for accurate context retrieval
- **💾 Persistent Storage**: Qdrant Cloud integration for permanent vector storage
- **📖 Source Citations**: Every answer includes page references for verification
- **💬 Interactive UI**: Clean, modern Streamlit interface with chat history
- **⚙️ Customizable Settings**: Adjust temperature and context chunks for optimal results
- **🌐 Cloud Deployment**: Fully deployed and accessible from anywhere

## 🏗️ Architecture

```
PDF Document → Text Extraction → Chunking → Embeddings → Vector DB (Qdrant)
                                                              ↓
User Query → Embedding → Similarity Search → Context Retrieval → LLM (Gemini) → Response
```

### Technology Stack

- **Frontend**: Streamlit
- **LLM**: Google Gemini 2.0 Flash
- **Embeddings**: Google Generative AI Embeddings (text-embedding-004)
- **Vector Database**: Qdrant Cloud
- **Framework**: LangChain
- **PDF Processing**: PyPDF

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google API Key ([Get one here](https://makersuite.google.com/app/apikey))
- Qdrant Cloud account ([Sign up](https://cloud.qdrant.io))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Saianeesh2003/pdf-chat-assistant.git
cd pdf-chat-assistant
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_google_api_key_here
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
```

4. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage

### Web Interface (Streamlit)

1. **Upload a PDF**: Click "Upload a PDF" in the sidebar
2. **Index the document**: Click "🔄 Index PDF" to process and store the document
3. **Start chatting**: Ask questions about your PDF in the chat input
4. **View sources**: Expand the "📄 View Sources" section to see relevant excerpts

### Command Line Interface

**Index a PDF:**
```bash
python index.py
```

**Chat with indexed PDF:**
```bash
python chat.py
```


### Chunking Strategy

```python
chunk_size = 1000      # Characters per chunk
chunk_overlap = 400    # Overlap between chunks
```

Optimize these values based on your document structure and query complexity.

## 📁 Project Structure

```
pdf-chat-assistant/
├── app.py                    # Streamlit web application
├── index.py                  # PDF indexing script
├── chat.py                   # Command-line chat interface
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── docker-compose.yml       # Docker configuration (for local Qdrant)
└── README.md                # Project documentation
```

## 🔧 Advanced Setup

### Using Local Qdrant (Docker)

If you prefer to run Qdrant locally:

1. **Start Qdrant with Docker Compose**
```bash
docker-compose up -d
```

2. **Update configuration**
```python
QDRANT_URL = "http://localhost:6333"
QDRANT_API_KEY = None
```

3. **Access Qdrant Dashboard**
Visit `http://localhost:6333/dashboard`

## 🌐 Deployment

This app is deployed on [Streamlit Cloud](https://streamlit.io/cloud). To deploy your own:

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add secrets in advanced settings:
   - `GOOGLE_API_KEY`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
5. Deploy!

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

- 🐛 Report bugs and issues
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit pull requests

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Google Gemini](https://deepmind.google/technologies/gemini/) for the powerful LLM
- [LangChain](https://langchain.com/) for the RAG framework
- [Qdrant](https://qdrant.tech/) for vector database
- [Streamlit](https://streamlit.io/) for the web framework

## 📧 Contact

**Your Name** - [@Saianeesh2003](https://github.com/Saianeesh2003)

Project Link: [https://github.com/Saianeesh2003/pdf-chat-assistant](https://github.com/Saianeesh2003/pdf-chat-assistant)

---

⭐ If you find this project helpful, please consider giving it a star!

## 🚀 Future Enhancements

- [ ] Support for multiple PDF uploads
- [ ] Conversation history persistence
- [ ] Export chat transcripts
- [ ] Support for Word documents and other formats
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Advanced search filters
- [ ] User authentication
- [ ] API endpoints for integration

## 📊 Performance

- **Average Response Time**: < 3 seconds
- **Supported PDF Size**: Up to 50MB
- **Concurrent Users**: Scalable with Streamlit Cloud
- **Vector Storage**: 1GB free tier on Qdrant Cloud

## 🔒 Security

- API keys stored as environment variables
- No sensitive data in repository
- Secure cloud deployment
- HTTPS encryption on Streamlit Cloud

## 📚 Learn More

- [RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)
- [Google Gemini Documentation](https://ai.google.dev/tutorials/python_quickstart)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Streamlit Documentation](https://docs.streamlit.io/)