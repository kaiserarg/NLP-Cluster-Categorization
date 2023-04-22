from keybert import KeyBERT
import json

kw_model = KeyBERT()

kw_model_multi = KeyBERT('paraphrase-multilingual-MiniLM-L12-v2')

f = open('rawData.json', "r")
keywordfile = open("keywords.json", "a")
count = 0
data = json.load(f)

keywords = {
}
 
for youtuber in data:
    if(data[youtuber]["corpus"] == ""):
            continue
    keyword = kw_model.extract_keywords(data[youtuber]["corpus"], top_n=10)
    keywords[data[youtuber]["name"]] = keyword
    count = count + 1
    print(count)

json.dump(keywords, keywordfile, indent=2)
    