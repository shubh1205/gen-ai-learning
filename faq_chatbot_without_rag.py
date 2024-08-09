import argparse
from openai import OpenAI

def create_client(access_key):
  """Creates an OpenAI client instance with the provided access key."""
  return OpenAI(api_key=access_key)

def load_documents(file_path):
  with open(file_path, 'r') as f:
    text = f.read()
  return [text]  # For simplicity, treating entire file as a single document

def generate_response(query, document, client):
  prompt = f"Provide a concise answer to the query: {query}\nUse the following information if relevant: {document}"
  response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
          {"role": "user", "content": prompt}
      ],
      max_tokens=1024,
      n=1,
      stop=None,
      temperature=0.5,
  )
  return response.choices[0].message.content

def chatbot(query, access_key):
  client = create_client(access_key)  # Create client using access_key
  documents = load_documents("faq.txt")
  # Implement basic retrieval logic (e.g., keyword matching) to find relevant documents
  relevant_document = documents[0]

  response = generate_response(query, relevant_document, client)
  return response

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Chatbot using OpenAI")
  parser.add_argument("--api_key", required=True, help="OpenAI API key")
  args = parser.parse_args()

  while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
      break
    response = chatbot(user_input, args.api_key)
    print("Chatbot:", response)
