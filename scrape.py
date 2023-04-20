from youtube_transcript_api import YouTubeTranscriptApi as transcriptAPI
from youtube_transcript_api.formatters import TextFormatter
import scrapetube
import json

formatter = TextFormatter()

youtubeURL = "https://www.youtube.com/@"
youtuberList = ["PewDiePie", "MrBeast", "WIRED"]
 
f = open("three-test-corpus.json", "a")

jsonDict = {}

for youtuber in youtuberList:
    videos = scrapetube.get_channel(None, youtubeURL + youtuber, 2, 1, "popular")
    corpus = ""
    for video in videos:
        try:
            transcriptList = transcriptAPI.get_transcript(video['videoId'])
            corpus = corpus + formatter.format_transcript(transcriptList, languages=['en', 'en-US']).replace("\n", " ")
        except Exception as e:
            continue
    
    #cleaning goes here
    jsonDict[youtuber] = {"name": youtuber, "corpus": corpus}

json.dump(jsonDict, f, indent=3)
f.close()