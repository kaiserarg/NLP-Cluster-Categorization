from keybert import KeyBERT
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import json

def clean(corpus):
    tokens = word_tokenize(corpus)
    lemmatizer = WordNetLemmatizer()
    tokens = [word.lower() for word in tokens]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return " ".join(tokens)


kw_model = KeyBERT()

kw_model_multi = KeyBERT('paraphrase-multilingual-MiniLM-L12-v2')

f = open('transcript_raw.json', "r")
keywordfile = open("keywords.json", "a")
count = 0
data = json.load(f)

keywords = {
}
 
for youtuber in data:
    if(data[youtuber]["corpus"] == ""):
            continue
    corpus = clean(data[youtuber]["corpus"])
    keyword = kw_model.extract_keywords(corpus, top_n=20)
    keywords[data[youtuber]["name"]] = keyword
    count = count + 1
    print(count)

json.dump(keywords, keywordfile, indent=2)
    