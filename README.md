# Chat with Documents

An AI-powered application that enables conversational interaction with documents in your local filesystem using natural language queries.

## Overview

This application scans documents in a specified directory (and its subdirectories), indexes them using vector embeddings, and allows you to ask questions about the content. The system retrieves relevant information and generates context-aware responses with source citations.

## Features

- **Recursive Document Discovery**: Automatically scans current directory and all subdirectories
- **Multi-Format Support**: Works with PDF, TXT, DOCX, MD, and other document formats
- **Vector-Based Search**: Uses semantic search to find relevant content
- **Natural Language Interface**: Ask questions in plain English
- **Source Citations**: Responses include references to source documents

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
   OPENAI_API_KEY=your_key_here
   ```

## Usage

```bash
python main.py
```

Then simply type your questions about the documents in the indexed directory.

## Project Structure

```
Chat with documents/
├── README.md
├── requirements.txt
├── design.txt           # Detailed design specification
├── src/                 # Source code
├── data/                # Document storage
└── tests/               # Test files
```

## How It Works

1. **Indexing**: Documents are loaded, chunked, and embedded into a vector database
2. **Query**: User submits a natural language question
3. **Retrieval**: Relevant document chunks are found via semantic search
4. **Generation**: LLM generates a response using the retrieved context
5. **Response**: Answer is displayed with source references

## Future Enhancements

- Real-time document monitoring and re-indexing
- Multi-language support
- Conversation history and follow-up questions
- Export chat transcripts
- Web-based UI

## Contributing

This is a learning project developed as part of the Python and AI Builders community.

## License

This project is for educational purposes.
