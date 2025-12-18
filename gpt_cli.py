import os
import sys
import argparse
from openai import OpenAI

# Path to store the token
TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".gpt_token")

def save_token(token):
    with open(TOKEN_FILE, "w") as f:
        f.write(token.strip())
    print("Token saved successfully.")

def load_token():
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, "r") as f:
        return f.read().strip()

def query_gpt(prompt):
    api_key = load_token()
    if not api_key:
        print("Error: API token not set.")
        print("Run 'gpt --token YOUR_KEY' to set it first.")
        return

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # You can change this to gpt-4 if you have access
            messages=[
                {"role": "system", "content": "You are a helpful CLI assistant. Keep answers concise."},
                {"role": "user", "content": prompt}
            ]
        )
        print("\n" + response.choices[0].message.content + "\n")
    except Exception as e:
        print(f"API Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Custom GPT CLI Tool")
    parser.add_argument("prompt", nargs="*", help="The text prompt for GPT")
    parser.add_argument("--token", help="Set the OpenAI API token", type=str)

    args = parser.parse_args()

    if args.token:
        save_token(args.token)
    elif args.prompt:
        # Join the list of words into a single string
        full_prompt = " ".join(args.prompt)
        query_gpt(full_prompt)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()