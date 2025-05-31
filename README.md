# 🎭 clown.ai

A witty AI storyteller that brings classic literature to life with humor, visual imagination, and interactive conversation. clown.ai combines the power of large language models with image generation to create an engaging storytelling experience based on classic works like *Alice in Wonderland*, *Gulliver's Travels*, and *Arabian Nights*.

## ✨ Features

- **📚 Story-Based Responses**: Generates humorous and witty answers using context from classic literature stored in a vector database
- **🎨 Visual Storytelling**: Creates accompanying images using Google's Vertex AI Imagen model to illustrate scenes and concepts
- **🔍 Semantic Search**: Uses Chroma vector database with embeddings to find relevant story passages
- **💬 Interactive Chat**: React-based frontend with follow-up questions to keep conversations engaging
- **🎭 Witty Personality**: AI responses are designed to be funny, clever, and descriptive with modern analogies and humor

## 🏗️ Architecture

### Backend (Python + FastAPI)
- **FastAPI** server handling API requests
- **Google Gemini 1.5 Pro** for text generation
- **Vertex AI Imagen 3.0** for image creation
- **Chroma DB** for vector storage and retrieval
- **HuggingFace Embeddings** for semantic search

### Frontend (React + Vite)
- **React 19** with modern hooks
- **Vite** for fast development and building
- **Lucide React** for icons
- **Responsive** chat interface

### Data Processing
- **PDF extraction** using pypdf
- **Text chunking** with LangChain splitters
- **Vector embeddings** using sentence-transformers

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- Google Cloud Platform account with Vertex AI enabled
- Gemini API key

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/kevin-joshua/clown.ai.git
   cd clown.ai
   ```

2. **Set up environment variables**
   ```bash
   export GEMINI_API_KEY="your_gemini_api_key"
   export PROJECT_ID="your_gcp_project_id"
   ```

### Backend Setup

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Add your story PDFs**
   - Place PDF files in the `pdfs/` directory
   - The system will automatically extract and index them on first run

3. **Start the FastAPI server**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   echo "VITE_API_BASE_URL=http://localhost:8000" > .env
   ```

4. **Start the development server**
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:5173`

## 📖 How It Works

### 1. Story Processing
- PDFs are extracted and chunked into manageable pieces (500 characters with 50-character overlap)
- Text chunks are embedded using `sentence-transformers/all-MiniLM-L6-v2`
- Embeddings are stored in Chroma vector database for fast retrieval

### 2. Query Processing
- User questions are processed using Maximum Marginal Relevance (MMR) search
- Relevant story passages are retrieved from the vector database
- Context is passed to the language model for response generation

### 3. Response Generation
- **Gemini 1.5 Pro** generates witty, humorous responses based on story context
- Responses avoid mentioning source stories directly for immersive experience
- Follow-up questions are automatically generated to continue conversation

### 4. Image Creation
- **Vertex AI Imagen 3.0** creates images based on story context and user query
- Images are generated only for informative responses (not for "I don't know" responses)
- Base64-encoded images are returned to the frontend

## 🛠️ API Endpoints

### POST /generate
Generate a response with optional image based on user prompt.

**Request Body:**
```json
{
  "prompt": "How does Gulliver attempt to communicate with the giants?"
}
```

**Response:**
```json
{
  "response": "Well, imagine trying to have a conversation with someone...",
  "image": "base64_encoded_image_data",
  "followup": [
    "What other challenges did Gulliver face with the giants?",
    "How did the giants react to Gulliver's attempts?"
  ]
}
```

## 📁 Project Structure

```
clown.ai/
├── pdfs/                    # PDF story files
├── chroma_db/              # Vector database storage
├── frontend/               # React application
│   ├── src/
│   │   ├── App.jsx        # Main React component
│   │   ├── App.css        # Styling
│   │   └── main.jsx       # Entry point
│   └── package.json       # Frontend dependencies
├── main.py                 # FastAPI server
├── llm.py                  # Language model logic
├── image_gen.py           # Image generation
├── retriever.py           # Vector search
├── story_loader.py        # PDF processing
└── requirements.txt       # Python dependencies
```

## 🎨 Key Technologies

- **[Google Gemini 1.5 Pro](https://ai.google.dev/)** - Advanced language model for text generation
- **[Vertex AI Imagen](https://cloud.google.com/vertex-ai/docs/generative-ai/image/overview)** - State-of-the-art image generation
- **[Chroma](https://www.trychroma.com/)** - Open-source vector database for AI applications
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework for building APIs
- **[React](https://react.dev/)** - Popular library for building user interfaces
- **[LangChain](https://langchain.com/)** - Framework for developing applications with LLMs

## 🔧 Configuration

### Model Parameters
- **Temperature**: 0.2 for consistent, focused responses
- **Max Output Tokens**: 512 for concise but detailed answers
- **Chunk Size**: 500 characters for optimal context retrieval
- **MMR Parameters**: λ=0.8, fetch_k=20 for diverse results

### Image Generation
- **Model**: imagen-3.0-fast-generate-001
- **Aspect Ratio**: 1:1 (square format)
- **Output Format**: PNG
- **Language**: English

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🎯 Future Enhancements

- [ ] Support for additional story formats (EPUB, TXT)
- [ ] Multi-language story support
- [ ] Voice narration capabilities
- [ ] Story recommendation system
- [ ] User story upload functionality
