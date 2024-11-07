# Asking questions from fine tuned model


``` py
from anoteai import Anote

api_key = 'INSERT_API_KEY_HERE'
Anote = Anote(api_key, isPrivate=False) #You can select isPrivate=True if you want to use private models

chat_id = Anote.upload(task_type="documents", model_type="gpt", file_paths=file_paths)['id']

file_paths = [
    'https://www.sec.gov/Archives/edgar/data/320193/000032019318000145/a10-k20189292018.htm',
    'https://www.sec.gov/Archives/edgar/data/320193/000119312514383437/d783162d10k.htm'
]

fine_tune_model_id = Anote.train(
    model_type="MLM",
    fine_tuning_type="unsupervised",
    document_files=file_paths
)['id']

response1 = Anote.chat(chat_id, "What is Apple's Revenue in 2023?" finetuned_model_key=fine_tuned_model_id)
print(response1['answer'])
print("Sources:", response1['sources'])

message_id1 = response1['message_id']
print(Anote.evaluate(message_id1))
```