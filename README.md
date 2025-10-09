# Chat with Documents

An AI-powered web application that enables conversational interaction with your documents using natural language queries through an intuitive Streamlit interface.

## Overview

This application provides a user-friendly web interface to chat with your documents. Enter a folder path in the sidebar, and the app will automatically index all supported documents. You can then ask questions about the content and receive AI-generated answers based on the document context, with full conversation history support.

## Features

- **Web-Based UI**: Clean, intuitive Streamlit interface with chat functionality
- **Folder Path Input**: Easy folder selection via text input with path validation
- **Recursive Document Discovery**: Automatically scans selected directory and all subdirectories
- **Multi-Format Support**: Works with PDF, TXT, DOCX, ODT. Other document formats will be added
- **Progress Tracking**: Visual progress bar during document indexing
- **Vector-Based Search**: Uses semantic search to find relevant content
- **Natural Language Interface**: Ask questions in plain English through chat interface
- **Conversation History**: Maintains context across multiple questions for follow-up queries
- **Chat Management**: Clear chat history with one click
- **Source Citations**: Responses include references to source documents
- **Comprehensive Test Suite**: 47 automated tests with 100% pass rate

## Technologies Used

- **Frontend**: Streamlit
- **LLM**: Google Gemini 2.5 Flash
- **Vector Database**: ChromaDB
- **Embeddings**: ChromaDB default embeddings
- **Framework**: LangChain
- **Document Processing**: PyPDF, python-docx, odfpy
- **Testing**: pytest with fixtures

## Installation

1. Clone this repository or download the files
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your API keys (create a `.env` file):
   ```
   GEMINI_API_KEY=your_key_here
   ```

## Usage

### Running the Application

Start the Streamlit web application:

```bash
streamlit run src/app.py
```

The application will open in your default web browser at `http://localhost:8501`.

### Using the Interface

1. **Enter Folder Path**: Type or paste the full path to your documents folder in the sidebar text input, then click "Load Folder"
2. **Wait for Indexing**: The app will automatically scan and index all supported documents (shows progress bar)
3. **Start Chatting**: Once indexing is complete, type your questions in the chat input at the bottom
4. **View Responses**: The AI will provide answers based on your documents, including source references
5. **Continue Conversation**: Ask follow-up questions - the chat maintains full conversation history
6. **Clear History**: Use the "Clear Chat History" button in the sidebar to start fresh

### CLI Version (Legacy)

A CLI version is also available:

```bash
python src/cli.py
```

## Project Structure

```
Chat with documents/
├── README.md
├── requirements.txt
├── pytest.ini                  # Test configuration
├── .env.example               # Environment variables template
├── src/                       # Source code
│   ├── app.py                # Main Streamlit web application
│   ├── cli.py                # CLI application (legacy)
│   ├── document_loader.py    # Document loading functions
│   ├── scan_folders.py       # Directory scanning
│   ├── vector_store.py       # Vector database operations
│   ├── retrieval_system.py   # Semantic search
│   ├── response_generator.py # LLM integration
│   └── utils.py              # Utility functions
├── tests/                     # Test suite (47 tests)
│   ├── test_utils.py
│   ├── test_scan_folders.py
│   ├── test_document_loader.py
│   └── test_vector_store.py
├── prompts/                   # LLM prompts
│   └── system.txt
└── data/                      # Your documents (not tracked)
```

## How It Works

1. **Indexing**: Documents are loaded, chunked, and embedded into a vector database
2. **Query**: User submits a natural language question
3. **Retrieval**: Relevant document chunks are found via semantic search
4. **Generation**: LLM generates a response using the retrieved context
5. **Response**: Answer is displayed with source references

## Testing

The project includes a comprehensive test suite with 47 automated tests covering core functionality.

### Running Tests

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Run all tests
pytest

# Run specific test file
pytest tests/test_utils.py

# Run with coverage report (optional)
pytest --cov=src
```

### Test Coverage

- **Document Loading**: Tests for TXT, PDF, DOCX, ODT formats with error handling
- **Directory Scanning**: Tests for recursive scanning, nested directories, and edge cases
- **Text Chunking**: Tests for document splitting, metadata generation, and indexing
- **Utility Functions**: Tests for filename sanitization and validation

All tests use pytest fixtures for isolated, repeatable testing with automatic cleanup.

## Future Enhancements

- Real-time document monitoring and re-indexing
- Multi-language support
- Export chat transcripts
- Support for additional document formats (Markdown, HTML, CSV)
- Document upload feature (in addition to folder selection)
- Streaming responses for better UX

## About

Developed as part of the Python & AI Builders community led by Ardit Sulce, this project explores practical AI integration in document processing and conversational interfaces using modern Python frameworks.

## License

This project is released under the MIT License.  
See the [LICENSE](./LICENSE) file for more details.
