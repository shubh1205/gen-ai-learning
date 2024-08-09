import argparse
from openai import OpenAI

def create_client(access_key):
  """Creates an OpenAI client instance with the provided access key."""
  return OpenAI(api_key=access_key)

# client = OpenAI(api_key="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")

def chat(user_message, access_key):
    client = create_client(access_key)  # Create client using access_key
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_message}
        ],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Chatbot using OpenAI")
  parser.add_argument("--api_key", required=True, help="OpenAI API key")
  args = parser.parse_args()

  while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
      break
    response = chat(user_input, args.api_key)
    print("Chatbot:", response)