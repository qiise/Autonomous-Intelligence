# Asking questions from websites


``` py
from anoteai import Anote

api_key = 'INSERT_API_KEY_HERE'
Anote = Anote(api_key, isPrivate=False) #You can select isPrivate=True if you want to use private models

file_paths = ['https://docs.Anote.ai/', 'https://docs.Anote.ai/10-ks/10ksbackground.html', 'https://docs.Anote.ai/api-overview/setup.html'] #'https://Anote.ai/faqs', 'https://Anote.ai/research']
chat_id = Anote.upload(task_type="documents", model_type="gpt", file_paths=file_paths)['id']

response1 = Anote.chat(chat_id, "What is Private Chatbot?")
print(response1['answer'])
print("Sources:", response1['sources'])

message_id1 = response1['message_id']
print(Anote.evaluate(message_id1))

print("-------------------------------------------------")

response2 = Anote.chat(chat_id, "Can you help me setup my local development environment?")
print(response2['answer'])
print("Sources:", response2['sources'])

message_id2 = response2['message_id']
print(Anote.evaluate(message_id2))
```

As an output we get (condensed for brevity):
```
Private Chatbot is a tool that enables enterprises to leverage generative AI and privacy preserving LLMs to engage with their documents while keeping their private data secure. It provides enterprises with their own AI assistant, that can answer any query based on their organizations' data. When members of the organization ask a question, the Private Chatbot uses a privacy-preserving retrieval component to search...
Sources: [['https://docs.Anote.ai/', "cally on the user's device or local infrastructure. These models preserve user privacy by avoiding the transmission of user queries or documents to external servers.Private ChatsAll queries stay on your computer, never leaving your private, secure data silo. Private Chatbot ensures that user queries and responses are kept private. When the user asks a question..."], ['https://docs.Anote.ai/', ' Table of contents        How is it Private?      Private Data      Private LLMs      Private Chats      How Does Private Chatbot Work?      Upload      Chat      Evaluate  Introduction to Private...']]
{'answer_relevancy': 0.9709236021067721, 'faithfulness': 1.0}
-------------------------------------------------
Yes, the text gives instructions on how to set up your local development environment. Here are the steps:

1. Generate an API key for your local system and make sure to save it somewhere safe. Remember not to share it with anyone.

2. Install Python in your system (if you don't have it yet). To check this, open your Terminal or Command line. For MacOS, find Terminal in the Applications folder or search for it using Spotlight (Command + Space). For Windows, open Command Prompt by searching "cmd" in the start menu. Verify your Python version by typing python3 --version and pressing enter. You should see a Python version higher than 3.7.

3. Install the Private Chatbot Python Library. In the terminal or command line, type in pip install -U Anote and press enter.

4. Sending your first API request. After configuring Python and setting up your API key, the next step is to send an API request to the Private Chatbot API using the Python library. To do this, create a file named Anote-test.py using the terminal or any Integrated Development Environment (IDE).
Sources: [['https://docs.Anote.ai/api-overview/setup.html', 'I key". Copy the API key, and make sure to save this somewhere safe and do not share it with anyone.Step 2: Installing Python Pip PackageTo use the Private Chatbot Python library, you need to have Python installed. To ensure you have Python installed, navigate to your Terminal... '], ['https://docs.Anote.ai/', 'Docs']]
{'answer_relevancy': 0.9084305015393235, 'faithfulness': 0.0}
```


