from dotenv import load_dotenv
import os
import sys

from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage

load_dotenv(override=True)


def set_llm():
    """
    Initialize and configure the Google Generative AI language model.

    Returns:
        GoogleGenerativeAI: Configured LLM instance with Gemini 2.5 Flash model.
    """
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY not found. Please set it in your .env file.")
        sys.exit(1)

    llm = GoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.2,
    )

    return llm


def generate_answer(llm, user_input, chunks, history):
    """
    Generate an answer to a user query using retrieved document chunks and chat history.

    Args:
        llm (GoogleGenerativeAI): The language model instance.
        user_input (str): The user's question or input text.
        chunks: Retrieved document chunks relevant to the query.
        history (list): List of previous chat messages (HumanMessage and AIMessage objects).

    Returns:
        str: The generated answer from the LLM.
    """
    try:
        with open("prompts/system.txt", "r", encoding="utf-8") as file:
            system_prompt = file.read()
    except FileNotFoundError:
        print("Error: Required system configuration file missing.")
        sys.exit(1)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("user", "{user_input}"),
        ]
    )

    chain = prompt | llm | StrOutputParser()

    try:
        answer = chain.invoke(
            {"user_input": user_input, "chunks": chunks, "history": history}
        )
    except Exception:
        print("Error calling Gemini API. This may be due to:")
        print("- Invalid GEMINI_API_KEY in your .env file")
        print("- Network connection issues")
        print("- API rate limits")
        sys.exit(1)

    return answer


def set_history(history, query, answer):
    """
    Update chat history with a new query-answer pair.

    Args:
        history (list or None): Existing chat history or None to create a new one.
        query (str): The user's query.
        answer (str): The generated answer.

    Returns:
        list: Updated chat history with the new messages appended.
    """
    if history is None:
        history = []

    history.append(HumanMessage(query))
    history.append(AIMessage(answer))

    return history


if __name__ == "__main__":
    import chromadb
    from retrieval_system import query_documents

    chroma_client = chromadb.PersistentClient(path="./vectordb")
    collection = chroma_client.get_or_create_collection(name="my_documents")

    query = "docx files"
    history = []

    results = query_documents(collection=collection, query_text=query, n_results=1)

    llm = set_llm()

    answer = generate_answer(llm=llm, user_input=query, chunks=results, history=history)
    history = set_history(history, query, answer)

    for item in history:
        print(item.content)
