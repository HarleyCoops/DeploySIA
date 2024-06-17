import os
import time
import openai
from typing import List
from dotenv import load_dotenv
from openai import OpenAI

import mesop as me
import mesop.labs as mel

# Load environment variables
load_dotenv()

# OpenAI API Configuration
openai.api_key = os.getenv('OPENAI_API_KEY')
if openai.api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable not set")
client = OpenAI()  

assistant_id = os.getenv('OPENAI_ASSISTANT_ID')
if assistant_id is None:
    raise ValueError("OPENAI_ASSISTANT_ID environment variable not set")

# Mesop Page Setup
@me.page(path="/chat", title="SIA 63")
def page():
    mel.chat(transform, title="SIA 63", bot_user="SIA 63")

# --- Core Assistant Interaction Logic ---
def transform(input: str, history: List[mel.ChatMessage]):
    try:
        # 1. Create a New Thread for the Conversation
        thread = client.beta.threads.create()

        # 2. Add User Message to the Thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=input,
        )

        # 3. Run the Assistant on the Thread
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id,
        )

        # 4. Retrieve and Yield Assistant's Responses
        yield from retrieve_and_yield_messages(thread.id, run.id) 

    except Exception as e:
        print(f"Error in transform function: {e}")
        yield ""  # Handle errors gracefully

# --- Helper Function to Fetch and Stream Responses --- 
def retrieve_and_yield_messages(thread_id, run_id):
    while True: 
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )

        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            for message in messages.data:
                if message.role == "assistant":
                    for content_block in message.content:
                        if content_block.type == 'text':
                            yield content_block.text.value + " "
            break  # Exit the loop once all messages are retrieved
        elif run.status in ["queued", "in_progress"]:
            time.sleep(1)  # Wait before checking again
        else:
            print(f"Unexpected run status: {run.status}")
            break  