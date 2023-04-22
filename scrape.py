from youtube_transcript_api import YouTubeTranscriptApi as transcriptAPI
from youtube_transcript_api.formatters import TextFormatter
import scrapetube
import json
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

formatter = TextFormatter()

youtubeURL = "https://www.youtube.com/@"

f = open("cleanedData.json", "a")

jsonDict = {}

for youtuber in youtuberList:
    videos = scrapetube.get_channel(None, youtuber[1], 10, 1, "popular")
    corpus = ""
    for video in videos:
        try:
            transcriptList = transcriptAPI.get_transcript(video['videoId'])
            corpus = corpus + formatter.format_transcript(transcriptList, languages=['en', 'en-US']).replace("\n", " ")
        except Exception as e:
            continue
    
    #cleaning goes here
    corpus = clean_corpus(corpus)
    jsonDict[youtuber[0]] = {"name": youtuber[0], "corpus": corpus}

json.dump(jsonDict, f, indent=3)
f.close()