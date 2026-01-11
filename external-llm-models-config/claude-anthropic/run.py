import os
import asyncio
from dotenv import load_dotenv
from anthropic import Anthropic, AsyncClient
import tiktoken

load_dotenv()

print(f"env var \"ANTHROPIC_API_KEY\": { os.getenv('ANTHROPIC_API_KEY', '')[:4] + '...' + os.getenv('ANTHROPIC_API_KEY', '')[-4:] if len(os.getenv('ANTHROPIC_API_KEY', '')) > 0 else 'NOT SET' }")
if not os.getenv('ANTHROPIC_API_KEY'):
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set. Please set it to your OpenAI API key.")

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
model = 'claude-haiku-4-5'

# Anthropic uses a tokenizer similar to p50k_base
# Note: This is an estimation for the ID list
encoding = tiktoken.get_encoding("p50k_base")

def get_token_data_input(text):
    """Gets ground-truth count from API and estimated IDs locally."""
    # 1. Official Ground Truth Count
    response = client.messages.count_tokens(
        model=model,
        messages=[{"role": "user", "content": text}]
    )
    count = response.input_tokens
    
    # 2. Estimated Token IDs
    token_ids = encoding.encode(text)
    return token_ids, count

def get_token_data_output(text):
    """Token IDs for model response (estimated IDs, exact count from usage)."""
    token_ids = encoding.encode(text)
    # Note: For output, the count is usually retrieved from the message.usage object
    return token_ids, len(token_ids)

# --- EXECUTION ---

# 1. User Request
user_input = "Tell the funny developer joke"
user_ids, user_count = get_token_data_input(user_input)

print(f"User: {user_input}")
print(f"> tokenized: {user_ids}")
print(f"> tokens count: {user_count}")

# 2. Get Model Response
message = client.messages.create(
    model=model,
    max_tokens=256,
    messages=[{"role": "user", "content": user_input}]
)

assistant_text = message.content[0].text
assistant_ids, _ = get_token_data_output(assistant_text)
# Official count for the response is provided in the usage object
assistant_count = message.usage.output_tokens

print(f"Assistant: {assistant_text}")
print(f"> tokenized: {assistant_ids}")
print(f"> tokens count: {assistant_count}")