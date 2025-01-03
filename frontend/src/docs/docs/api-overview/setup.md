# Overview

The Anote API is a software developer kit designed for developers to leverage LLMs to train models, make predictions and evaluate the output. There are 3 main API endpoints:

- **Train:** Train / Fine Tune LLM.

- **Predict:** Do Model Inference on Trained / Zero Shot Models.

- **Evaluate:** Evaluate different LLMs to measure performance.

## Setup

This setup guide is designed to help get your local development environment setup and send your first API request. Throughout this guide, you will learn:

- How to setup your Anote account
- How to install the Anote Python Pip Package
- How to send your first Anote API request

### Step 1: Account setup

First, create an Anote (https://anote.ai/) account or sign in. Next, navigate to the API key page and press the **Create new API key** button to generate a new API key.

![tweets](../assets/new_assets/APIKeys.png)

Copy the API key, and make sure to save this somewhere safe and do not share it with anyone.

### Step 2: Installing Python Pip Package

To use the Anote Python library, you need to have Python installed. To ensure you have Python installed, navigate to your Terminal or Command line:

- MacOS: **Open Terminal:** You can find it in the Applications folder or search for it using Spotlight (Command + Space).

- Windows: **Open Command Prompt:** You can find it by searching "cmd" in the start menu.

Next, enter ```python3 --version``` and then press enter, to ensure you see a python version >3.7.

To install the Private Chatbot Python library from the terminal / command line, run:
``` py
pip install -U anoteai
```

### Step 3: Sending your first API request

After you have Python configured and set up an API key, the final step is to send a request to the Anote API using the Python library. To do this, create a file named anote-test.py using the terminal or an IDE.

Inside the file, copy and paste the example below:
``` py
from anoteai import Anote

api_key = 'INSERT_API_KEY_HERE'
anote = Anote(api_key, isPrivate=True)
```
You should obtain an anote object.

### Supported Models and Tasks

The code below contains the supported model types, task types, and evaluation metrics in our current SDK.

::: fsdk.anote-sdk.NLPTask
    <!-- options:
        show_source: false -->

::: fsdk.anote-sdk.ModelType
    <!-- options:
        show_source: false -->

::: fsdk.anote-sdk.ZeroShotModelType
    <!-- options:
        show_source: false -->

::: fsdk.anote-sdk.EvaluationMetric
    <!-- options:
        show_source: false -->

The Private Chatbot API is a software developer kit designed for developers to leverage Private LLMs to upload documents, chat with them and evaluate the answers. There are 3 API endpoints:

- **Upload:** Upload documents or specify a ticker for data retrieval and Q&A.

- **Chat:** Send a message to the chatbot based on documents previously uploaded.

- **Evaluate:** Evaluate predictions on one or multiple documents/text.

## Setup

This setup guide is designed to help get your local development environment setup and send your first API request. Throughout this guide, you will learn:

- How to setup your Private Chatbot account
- How to install the Private Chatbot Python Pip Package
- How to send your first Private Chatbot API request

### Step 1: Account setup

First, create an Private Chatbot (https://Anote.ai/) account or sign in. Next, navigate to the API key page and "Create new API key". Copy the API key, and make sure to save this somewhere safe and do not share it with anyone.

### Step 2: Installing Python Pip Package

To use the Private Chatbot Python library, you need to have Python installed. To ensure you have Python installed, navigate to your Terminal or Command line:

- MacOS: **Open Terminal:** You can find it in the Applications folder or search for it using Spotlight (Command + Space).

- Windows: **Open Command Prompt:** You can find it by searching "cmd" in the start menu.

Next, enter ```python3 --version``` and then press enter, to ensure you see a python version >3.7.

To install the Private Chatbot Python library from the terminal / command line, run:
``` py
pip install -U Anote
```

### Step 3: Sending your first API request

After you have Python configured and set up an API key, the final step is to send a request to the Private Chatbot API using the Python library. To do this, create a file named Anote-test.py using the terminal or an IDE. Download these documents and move them to your local directory.

Now, you have two choices: you can either use the private models (LLaMa or Mistral), or you can use the public models (GPT-4 or Claude).

If you want to use private models, inside the file, copy and paste the example below:
``` py
from anoteai import Anote

api_key = 'INSERT_API_KEY_HERE'
Anote = Anote(api_key, isPrivate=True)

file_paths = ['doc1.pdf', 'doc2.pdf']

upload_result = Anote.upload(task_type="documents", model_type="llama", file_paths=file_paths)
print("output from upload: ", upload_result)
chat_id = upload_result['id']
chat_result = Anote.chat(chat_id, "What is this paper classification performance about?")
print("output from chat: ", chat_result)
message_id = chat_result['message_id']
print("output from evaluate:", Anote.evaluate(message_id))
```

If you want to use public models, inside the file, copy and paste the example below:
``` py
from anoteai import Anote

api_key = 'INSERT_API_KEY_HERE'
Anote = Anote(api_key, isPrivate=False)

file_paths = ['doc1.pdf', 'doc2.pdf']

upload_result = Anote.upload(task_type="documents", model_type="gpt", file_paths=file_paths)
print("output from upload: ", upload_result)
chat_id = upload_result['id']
chat_result = Anote.chat(chat_id, "What is this paper classification performance about?")
print("output from chat: ", chat_result)
message_id = chat_result['message_id']
print("output from evaluate:", Anote.evaluate(message_id))
```

If you want to use both private and public models, inside the file, copy and paste the example below:
``` py
from anoteai import Anote

api_key = 'INSERT_API_KEY_HERE'
Anote_private = Anote(api_key, isPrivate=True)
Anote_public= Anote(api_key, isPrivate=False)


file_paths = ['doc1.pdf', 'doc2.pdf']

upload_result = Anote_private.upload(task_type="documents", model_type="llama", file_paths=file_paths)
print("output from upload private: ", upload_result)
chat_id = upload_result['id']
chat_result = Anote_private.chat(chat_id, "What is this paper classification performance about?")
print("output from chat private: ", chat_result)
message_id = chat_result['message_id']
print("output from evaluate private:", Anote_private.evaluate(message_id))

upload_result = Anote_public.upload(task_type="documents", model_type="gpt", file_paths=file_paths)
print("output from upload public: ", upload_result)
chat_id = upload_result['id']
chat_result = Anote_public.chat(chat_id, "What is this paper classification performance about?")
print("output from chat public: ", chat_result)
message_id = chat_result['message_id']
print("output from evaluate public:", Anote_public.evaluate(message_id))
```

To run the code, enter ```python Anote-test.py``` into the terminal. The output should look as follows (may differ slightly depending on whether you have selected private/public):

```
output from upload:  {'id': 49}
output from chat:  {'answer': 'This paper, "Improving Classification Performance With Human Feedback", is about enhancing the accuracy, recall, and precision of AI models with the help of human feedback', 'message_id': 87, 'sources': ['doc1.pdf', 'Improving Classification Performance With Human Feedback:\n\nLabel a few, we label the rest\n\nEden Chung, Liang Zhang, Katherine Jijo, Thomas Clifford, Natan Vidra\n\nAbstract\n\nIn the realm of artificial intelligence, where a vast majority of data is unstructured']}
output from evaluate: {'answer_relevancy': 0.887419956065742, 'faithfulness': 1.0}
```


api-overview/setup.md
markdown
Copy code
# AI Agent SDK: Overview & Setup

Welcome to the **AI Agent SDK**! This document provides the necessary steps to get you started using the `anote-agents` package.

## 1. Installation

If the SDK is hosted on PyPI:

```bash
pip install anote-agents
If it’s hosted on a private repository, follow the specific instructions provided by your organization (e.g., credentials, pip index URL, or Git-based install).

2. Requirements
Python 3.8+
(Optional) API key for certain integrated tools or private LLM endpoints
(Optional) Additional service credentials (e.g., scraping, web search)
3. Configuration
3.1 Environment Variables
Common environment variables might include:

API_KEY for accessing private or third-party services
MODEL_KEY if specifying a private or custom LLM
3.2 Project Structure
A typical project setup might look like:

bash
Copy code
my_project/
  ├─ main.py
  ├─ requirements.txt
  ├─ .env
  └─ ...
Use .env (with python-dotenv) or other secure methods to store sensitive keys.

4. Basic Usage Example
python
Copy code
from anote_agents import Agent, Task, Crew

# Simple Agent
basic_agent = Agent(role="Greeting Agent", goal="Greet the world")

# Simple Task
greet_task = Task(description="Say hello", agent=basic_agent)

# Crew that ties everything together
crew = Crew(agents=[basic_agent], tasks=[greet_task])

result = crew.kickoff()
print(result)  # Agent responds with a greeting
This snippet demonstrates the most basic workflow:

Agent definition
Task definition
Crew orchestration
That’s all you need to start exploring the AI Agent SDK!