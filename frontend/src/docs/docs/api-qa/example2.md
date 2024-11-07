# Asking questions from Uploaded Documents

``` py
from anoteai import Anote

api_key = 'INSERT_API_KEY_HERE'
Anote = Anote(api_key, isPrivate=True) #You can select isPrivate=False if you want to use private models

chat_id = Anote.upload(task_type="documents", model_type="mistral", file_paths=file_paths)['id']

response = Anote.chat(chat_id, "What does this company do?")
print(response['answer'])
print("Sources:", response['sources'])

message_id = response['message_id']
print(Anote.evaluate(message_id))
```

As an output we get:
```
The research paper "Improving Classification Performance With Human Feedback" is written by Eden Chung, Liang Zhang, Katherine Jijo, Thomas Clifford, and Natan Vidra.
Sources: [['Anote_research_paper.pdf', 'Improving Classification Performance With Human Feedback:\n\nLabel a few, we label the rest\n\nEden Chung, Liang Zhang, Katherine Jijo, Thomas Clifford, Natan Vidra\n\nAbstract\n\nIn the realm of artificial intelligence, where a vast majority of data is unstructured, obtaining sub-\nstantial amounts of labeled data to train supervised machine learning models poses a significant\nchallenge. To address this, we delve into few-shot and active learning, where are goal is to improve\nAI models with human feedback on a few labeled examples. This paper focuses on understanding how\na continuous feedback loop can refine models, thereby enhancing their accuracy, recall, and precision\nthrough incremental human input. '], ['Anote_research_paper.pdf', 'By employing Large Language Models (LLMs) such as GPT-3.5,\nBERT, and SetFit, we aim to analyze the efficacy of using a limited number of labeled examples to\nsubstantially improve model accuracy. We benchmark this approach on the Financial Phrasebank,Banking, Craigslist, Trec, Amazon Reviews da']]
{'answer_relevancy': 0.9307434918423216, 'faithfulness': 1.0}
```