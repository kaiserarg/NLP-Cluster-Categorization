import nltk
import string
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from youtuberlist import youtuberList
from nltk import re

def clean_corpus(corpus):
    tokens = word_tokenize(corpus)
    tokens = [word.lower() for word in tokens]
    
    #remove words in corpus with parenthesis around them, in the youtube transcript this would filter out (laughs) or (music playing)
    tokens = [re.sub(r'\([^)]*\)', '', word) for word in tokens]
    #remove punctuation
    tokens = [word for word in tokens if word not in string.punctuation]
    #remove words like 's --> for some reason the tokenizer splits up words like dog's into dog and 's 
    tokens = [word for word in tokens if not any(char in string.punctuation for char in word)]
    tokens = [word for word in tokens if word not in ('”', '“', '’', '‘')]
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.lower() not in stop_words]
    lemmatizer = WordNetLemmatizer()

    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    string_of_tokens = ' '.join(tokens)

    return string_of_tokens
