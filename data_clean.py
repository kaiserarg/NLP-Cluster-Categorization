import nltk
import string
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from youtuberlist import youtuberList

def clean_corpus(corpus):
    tokens = word_tokenize(corpus)
    tokens = [word.lower() for word in tokens]
   
    tokens = [word for word in tokens if not any(char in ('(', ')') for char in word)]
    tokens = [word for word in tokens if word not in string.punctuation]
    tokens = [word for word in tokens if not any(char in string.punctuation for char in word)]
    tokens = [word for word in tokens if word not in ('”', '“', '’', '‘')]
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.lower() not in stop_words]
    lemmatizer = WordNetLemmatizer()

    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    string_of_tokens = ' '.join(tokens)

    return string_of_tokens
