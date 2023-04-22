import nltk
import string
from stop_list import closed_class_stop_words
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import re
import json


f= open("cleanedData.json", "r")

data = json.load(f)
cleaned_data = {}

for youtuber in data:
    corpus = data[youtuber]["corpus"]

    tokens = word_tokenize(corpus)
    tokens = [word.lower() for word in tokens]

    #remove stop words from assignment4
    tokens = [word for word in tokens if word not in closed_class_stop_words]
    #remove things (laughter)
    tokens = [word for word in tokens if not any(char in '(' for char in word)] 
    #remove punctuation
    tokens = [word for word in tokens if word not in string.punctuation]

    #remove common exclamations
    tokens = [re.sub(r'(oh.*)|(hah.*)|(ah.*)|(yee.*)|(uh.*)|(hm.*)|(shh.*)|(umm.*)', '', word) for word in tokens] 

    #remove words like 's --> for some reason the tokenizer splits up words like dog's into dog and 's 
    tokens = [word for word in tokens if not any(char in (string.punctuation) for char in word)]

    tokens = [word for word in tokens if word not in ('”', '“', '’', '‘', 'yes', 'no', 'ugh', 'really', 'eh', 'gon', 'na', 'wow', 'wan', 'yep'
                                                      'na', 'hey', 'phew', 'u', 'le', 'ca', 'bl', 'hum', 'um', 'ye', 'sh', 'yay', 'yo'
                                                      'ok', 'okay', 'hi', 'hello')]


    
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.lower() not in stop_words]
    
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    string_of_tokens = ' '.join(tokens)
    #remove all unicode characters like "\u00e9", "\u2026", "\u00fc"
    string_of_tokens = ''.join(char for char in string_of_tokens if ord(char) < 128)
    #remove numbers
    string_of_tokens = ''.join(char for char in string_of_tokens if not char.isdigit())

    cleaned_data[youtuber] = {"corpus": string_of_tokens}

with open("new_clean_data.json", "w") as output:
    json.dump(cleaned_data, output, indent=1)
    
