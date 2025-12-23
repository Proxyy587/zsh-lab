# import os
# import sys
# import argparse
# from openai import OpenAI

# TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".gpt_token")
# MODEL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".gpt_model")

# AVAILABLE_MODELS = [
#     "gpt-3.5-turbo",
#     "gpt-4",
#     "gpt-4-turbo",
#     "gpt-4o",
#     "gpt-4o-mini"
# ]

# def save_token(token):
#     with open(TOKEN_FILE, "w") as f:
#         f.write(token.strip())
#     print("Token saved successfully.")

# def load_token():
#     if not os.path.exists(TOKEN_FILE):
#         return None
#     with open(TOKEN_FILE, "r") as f:
#         return f.read().strip()

# def save_model(model):
#     if model not in AVAILABLE_MODELS:
#         print(f"Model '{model}' is not recognized. Run 'gpt --list-models' to see available models.")
#         return
#     with open(MODEL_FILE, "w") as f:
#         f.write(model)
#     print(f"Default model set to '{model}'.")

# def load_model():
#     if not os.path.exists(MODEL_FILE):
#         return "gpt-4o-mini"
#     with open(MODEL_FILE, "r") as f:
#         model = f.read().strip()
#     if model not in AVAILABLE_MODELS:
#         return "gpt-4o-mini"
#     return model

# def list_models():
#     print("Available models:")
#     for m in AVAILABLE_MODELS:
#         marker = ""
#         if m == load_model():
#             marker = " (default)"
#         print(f"  {m}{marker}")

# def query_gpt(prompt, model=None):
#     api_key = load_token()
#     if not api_key:
#         print("Error: API token not set.")
#         print("Run 'gpt --token YOUR_KEY' to set it first.")
#         return

#     if model is None:
#         model = load_model()

#     client = OpenAI(api_key=api_key)

#     try:
#         response = client.chat.completions.create(
#             model=model,
#             messages=[
#                 {"role": "system", "content": "You are a helpful CLI assistant. Keep answers concise."},
#                 {"role": "user", "content": prompt}
#             ]
#         )
#         print("\n" + response.choices[0].message.content + "\n")
#     except Exception as e:
#         print(f"API Error: {e}")

# def main():
#     parser = argparse.ArgumentParser(description="Custom GPT CLI Tool")
#     parser.add_argument("prompt", nargs="*", help="The text prompt for GPT")
#     parser.add_argument("--token", help="Set the OpenAI API token", type=str)
#     parser.add_argument("--list-models", action="store_true", help="List all available GPT models")
#     parser.add_argument("--set-model", type=str, help="Set the default GPT model")
#     parser.add_argument("--model", type=str, help="Use this model for this query only")

#     args = parser.parse_args()

#     if args.token:
#         save_token(args.token)
#     elif args.list_models:
#         list_models()
#     elif args.set_model:
#         save_model(args.set_model)
#     elif args.prompt:
#         full_prompt = " ".join(args.prompt)
#         model = args.model if args.model else None
#         query_gpt(full_prompt, model)
#     else:
#         parser.print_help()

# if __name__ == "__main__":
#     main()