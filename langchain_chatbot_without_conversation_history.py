import argparse
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from uuid import uuid4
from pinecone import Pinecone

def load_documents(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    return text  # For simplicity, treating entire file as a single document

def chatbot(query, openai_api_key, pinecone_api_key, pinecone_index_name, embedding_model="text-embedding-ada-002"):
    # Load documents and adjust chunking strategy as needed
    raw_text = load_documents("faq.txt")
    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )

    documents = text_splitter.create_documents([raw_text])  # Assuming documents is a list with single element
    uuids = [str(uuid4()) for _ in range(len(documents))]
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model=embedding_model)

    # Create vector store
    pc = Pinecone(api_key=pinecone_api_key)
    index = pc.Index(pinecone_index_name)
    vectorstore = PineconeVectorStore(index=index, embedding=embeddings)
    vectorstore.add_documents(documents, ids=uuids)
    retriever = vectorstore.as_retriever()

    # Create retrieval QnA chain
    llm = OpenAI(openai_api_key=openai_api_key, temperature=0.7)
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    response = rag_chain.invoke({"input": query})
    return response['answer']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chatbot using OpenAI and Pinecone")
    parser.add_argument("--openai_api_key", required=True, help="OpenAI API key")
    parser.add_argument("--pinecone_api_key", required=True, help="Pinecone API key")
    parser.add_argument("--pinecone_index_name", default="langchain-index", required=True, help="Pinecone index name")
    parser.add_argument("--embedding_model", default="text-embedding-ada-002", help="OpenAI embedding model")
    args = parser.parse_args()

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        response = chatbot(user_input, args.openai_api_key, args.pinecone_api_key, args.pinecone_index_name, args.embedding_model)
        print("Chatbot:", response)
