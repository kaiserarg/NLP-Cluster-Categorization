import nltk
import string
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

def preprocess_corpus(corpus):
    tokens = word_tokenize(corpus)
    tokens = [word.lower() for word in tokens]

    # Remove punctuation from tokens
    tokens = [word for word in tokens if word not in string.punctuation]
    lemmatizer = WordNetLemmatizer()

    # Lemmatize tokens to their base form (singularize)
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return tokens

with open("clean_corpus.py", "r") as file:
    tokens = preprocess_corpus(file)