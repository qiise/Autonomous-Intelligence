# Uploading documents in different languages

``` py
from anoteai import Anote

api_key = 'INSERT_API_KEY_HERE'
Anote = Anote(api_key, isPrivate=False) #You can select isPrivate=True if you want to use private models

file_paths = ['jap1.pdf', 'en1.pdf']
chat_id = Anote.upload(task_type="documents", model_type="claude", file_paths=file_paths)['id']

response_english = Anote.chat(chat_id, "What is the Roy Hill Iron Ore Project?")
print(response_english['answer'])
print("Sources:", response_english['sources'])

message_id_eng = response_english['message_id']
print(Anote.evaluate(message_id_eng))

print("-------------------------------------------------")

response_japanese = Anote.chat(chat_id, "何ですかロイヒル鉄鉱山プロジェクト?")
print(response_japanese['answer'])
print("Sources:", response_japanese['sources'])

message_id_jap = response_japanese['message_id']
print(Anote.evaluate(message_id_jap))
```

As an output we get (condensed for brevity):
```
The Roy Hill Iron Ore Project is an operation in Australia that actively introduces advanced technologies to streamline its processes, from iron ore exploration and mining to shipping at ports, enhancing its competitiveness...
Sources: [['en1.pdf', 'ss\n\nCase① ： Australia ｜ Roy Hill Iron Ore Project\n\n▲\n\nRoy Hill iron ore project proactively applies cutting-edge technolo-\ngies to seamlessly streamline their operation process, from iron ore \nexploration/mining to shipping from ports, and to improve their com-\npetitiveness.▲\n\nThe operation center in Perth...'], ['en1.pdf, '(located 1,300 km away from the mine site)▲\n\nAn unmanned, fully autonomous haulage system will soon be \ndeployed for heavy dump trucks. This add-on system provides retro-\nfit capabilities to automate dump trucks of different manufacturers. \nThrough collaboration with a U.S. startup company']]
{'answer_relevancy': 0.9534500905980047, 'faithfulness': 0.8571428571428571}
-------------------------------------------------
ロイヒル鉄鉱山プロジェクトは、豪州に位置していて最新技術の積極的な導入により、鉄鉱石の探査・採掘から港湾での出荷までをシームレスに最適化し競争力を強化しています。パース市にあるリモートオペレーションセンターで、鉄鉱石の採掘から港湾での船積みまでをリアルタイムで遠隔管理していま...
Sources: [['jap1.pdf', '\n豪州Roy Hill鉄鉱山プロジェクトにて、最新技術の積極導入により、鉄鉱\n石の探査・採掘から港湾での出荷までをシームレスに最適化することで競\n争力を強化している。▲\n\nパース...'], ['jap1.pdf', 'への変貌\n\n\n\n15\n\nGC2021 DX\nGlobal crossvalue platform\n\n銅鉱山事業の自動化・DX\n\n事例② ： チリ ｜ Antofagasta社とのチリ銅鉱山事業\n\n▲\n\nAntofagasta社とのチリ銅鉱...']]
{'answer_relevancy': 0.7301118502936456, 'faithfulness': 0.75}
```

Our model will be able to detect what language your question is in and find chunks from the relevant document accordingly.