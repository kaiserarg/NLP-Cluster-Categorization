from keybert import KeyBERT
import json

kw_model = KeyBERT()

kw_model_multi = KeyBERT('paraphrase-multilingual-MiniLM-L12-v2')

f = open('cleanedData.json')

data = json.load(f)
  
for youtuber in data:
    keywords = kw_model.extract_keywords(data[youtuber]["corpus"], top_n=10)
    print(keywords)