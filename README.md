# Chat with Documents

An AI-powered application that enables conversational interaction with documents in your local filesystem using natural language queries.

## Overview

This application scans documents in a specified directory (and its subdirectories), indexes them using vector embeddings, and allows you to ask questions about the content. The system retrieves relevant information and generates context-aware responses with source citations.

## Features

- **Recursive Document Discovery**: Automatically scans current directory and all subdirectories
- **Multi-Format Support**: Works with PDF, TXT, DOCX, ODT. Other document formats will be added
- **Vector-Based Search**: Uses semantic search to find relevant content
- **Natural Language Interface**: Ask questions in plain English
- **Conversation History**: Maintains context across multiple questions for follow-up queries
- **Source Citations**: Responses include references to source documents
- **Comprehensive Test Suite**: 47 automated tests with 100% pass rate

## Technologies Used

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

```bash
python src/cli.py
```

Example interaction:
```
Enter directory to scan (default: data): data
Directory used: 'data'
Oct 07, 2025 14:30:15

Ask a question (or type 'exit' to quit): What are the main topics covered in the documents?
Based on the documents, the main topics include...

Ask a question (or type 'exit' to quit): exit
```

## Project Structure

```
Chat with documents/
├── README.md
├── requirements.txt
├── pytest.ini                  # Test configuration
├── .env.example               # Environment variables template
├── src/                       # Source code
│   ├── cli.py                # Main CLI application
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
- Web-based UI
- Support for additional document formats (Markdown, HTML, CSV)

## Contributing

This is a learning project developed as part of the Python and AI Builders community.

## License

This project is for educational purposes.
