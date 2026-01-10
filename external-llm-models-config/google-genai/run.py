from google import genai
from google.genai import types
import os

from dotenv import load_dotenv

load_dotenv()

# if set, print first 4 chars and last 4 chars and dots inside, else print NOT SET
print(
    f"env var \"GEMINI_API_KEY\" is: { os.getenv('GEMINI_API_KEY', '')[:4] + '...' + os.getenv('GEMINI_API_KEY', '')[-4:] if len(os.getenv('GEMINI_API_KEY', '')) > 0 else 'NOT SET' }"
)
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError(
        "GEMINI_API_KEY environment variable is not set. Please set it to your Google Gemini API key."
    )

client = genai.Client()

model = "gemini-2.5-flash"

# generate content using the model and get the response
# response = client.models.generate_content(
#     model=model, contents="What is the capital of France?"
# )

# print(response.text)

################################################################################

# Define specific configuration
# coder_config = types.GenerateContentConfig(
#     temperature=0.1, top_p=0.95, max_output_tokens=150
# )

# response = client.models.generate_content(
#     model="gemini-2.0-flash",
#     contents="What is the capital of France?",
#     config=coder_config,
# )

# print(response.text)

################################################################################

# Define a system role and conversation history
# system_role = "you were Gandalf the Grey in the Lord of the Rings. You answer in max 15 words. Your answers are mysterious and magical."

# conversation_history = [
#     types.Content(
#         role="user",
#         parts=[types.Part.from_text(text="What is the best time for coffee?")]
#     ),
#     types.Content(
#         role="model",
#         parts=[types.Part.from_text(text="The best time for coffee is in the morning my apprentice.")]
#     ),
#     types.Content(
#         role="user",
#         parts=[types.Part.from_text(text="How about tea?")]
#     ),
# ]

# response = client.models.generate_content(
#     model=model,
#     contents=conversation_history,
#     config=types.GenerateContentConfig(
#         system_instruction=system_role,
#         thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
#     ),
# )

# print(response.text)

################################################################################

#compute_tokens is not supported for Gemini Developer Api
def get_tokens_info(text):
    response = client.models.compute_tokens(
        model=model,
        contents=text
    )
    # Extract IDs from all token_info parts
    token_ids = []
    for info in response.tokens_info:
        if info.token_ids:
            token_ids.extend(info.token_ids)
            
    return token_ids, response.total_tokens

def get_tokens_count(text):
    response = client.models.count_tokens(
        model=model,
        contents=text
    )

    return response.total_tokens
    

# 1. User Request
user_input = "What is the capital of France?"
user_count = get_tokens_count(user_input)

print(f"User: {user_input}")
print(f"> tokenized: NOT SUPPORTED FOR DEVELOPER API")
print(f"> tokens count: {user_count}")

# 2. Get Model Response
response = client.models.generate_content(
    model=model,
    contents=user_input
)
assistant_text = response.text

# 3. Tokenize Model Response
assistant_count = get_tokens_count(assistant_text)

print(f"Assistant: {assistant_text}")
print(f"> tokenized: NOT SUPPORTED FOR DEVELOPER API")
print(f"> tokens count: {assistant_count}")