# Asking questions from Apple's 10-K

``` py
from anoteai import Anote

api_key = 'INSERT_API_KEY_HERE'
Anote = Anote(api_key, isPrivate=False) #You can select isPrivate=True if you want to use private models

chat_id = Anote.upload(task_type="edgar", model_type="gpt", ticker="aapl")['id']

response = Anote.chat(chat_id, "What does this company do?")
print(response['answer'])

message_id = response['message_id']
print(Anote.evaluate(message_id))
```

As an output we get:
```
Apple is a technology company continually improves its
products and services via researching and developing
new technologies hardware devices, accessories, software, and services.
{'answer_relevancy': 0.8, 'faithfulness': 0.9}
```