import mlflow
import os
from openai import OpenAI


# --- OpenAI Client Configuration (for local server communication) ---
# An API key is not strictly needed, but the client requires a Base URL to be passed
# The Base URL points to the locally running Llama.cpp server

LLAMA_CPP_SERVER = {
    "engine": "llama-cpp",
    "model": "whatever-model", # you can put whatever you want here, because on this URL there is only one model
    "base_url": "http://localhost:8080/v1",
}
# ==========================================
# 1. Configuration & Orchestration Setup
# ==========================================

# Define the location where MLflow will store tracking data.
# We use a local directory './mlruns' for simplicity.
# mlflow.set_tracking_uri("file:./mlruns")

# We use the default MLflow UI port (5000)
mlflow.set_tracking_uri("http://127.0.0.1:5000/")

# Define the specific Experiment name.
# This groups all your runs (prompts) under one dashboard entry.
experiment_name = f"Local_Model_Monitor_{LLAMA_CPP_SERVER['engine']}"
mlflow.set_experiment(experiment_name)

print(f"--> MLflow Experiment set to: {experiment_name}")

# ==========================================
# 2. Configure the Client (OpenAI Compatible)
# ==========================================

# Point the OpenAI client to the local llama.cpp server.
# Llama.cpp default port is 8080.
# The 'v1' suffix is required for OpenAI compatibility.
client = OpenAI(
    base_url=LLAMA_CPP_SERVER["base_url"], 
    api_key="sk-no-key-required" # Llama.cpp requires a string, but doesn't validate it.
)

# ==========================================
# 3. Enable MLflow Autologging
# ==========================================

# This is the "magic" command. It tells MLflow to watch the 'openai' library.
# It will automatically capture:
# - The prompt sent
# - The response received
# - Parameters (temperature, tokens, etc.)
mlflow.openai.autolog()

# ==========================================
# 4. Execute the Interaction
# ==========================================

print("--> Sending request to local Llama.cpp model...")

# We start a specific run to capture this interaction.
with mlflow.start_run() as run:
    print(f"Tracking started in MLflow Run ID: {run.info.run_id}")

    # Define the system and user message
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Explain the concept of 'Recursion' in one sentence."}
    ]
    
    try:
        # Send the request to the local model
        response = client.chat.completions.create(
            model=LLAMA_CPP_SERVER["model"], # The name here is often ignored by llama.cpp, but required by the library
            messages=messages,
            temperature=0.7,
            max_tokens=150,
        )

        # Extract the actual text response
        ai_reply = response.choices[0].message.content
        
        print("\n[Model Response]:")
        print(ai_reply)
    except Exception as e:
        print(f"Error connecting to the model: {e}")
        print(f"Make sure the {LLAMA_CPP_SERVER['engine']}.server is running at {LLAMA_CPP_SERVER['base_url']}.")
        mlflow.end_run(status="failed")

    # Note: Because autolog() is enabled, we do not need to manually log params or metrics.
    # MLflow handles saving the 'messages' and the 'response' object automatically.
    # The interaction data (prompt, response, parameters, tokens) is now
    # automatically logged as a 'Trace' in MLflow thanks to autologging.

    print(f"\nThe Trace is available in the MLflow UI in the 'Traces' section for Run ID: {run.info.run_id}")