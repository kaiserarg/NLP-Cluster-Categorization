from youtube_transcript_api import YouTubeTranscriptApi as transcriptAPI
from youtube_transcript_api.formatters import TextFormatter
import scrapetube
import json
from youtuberlist import youtuberList

formatter = TextFormatter()

youtubeURL = "https://www.youtube.com/@"

f = open("rawData.json", "a")

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
    jsonDict[youtuber[0]] = {"name": youtuber[0], "corpus": corpus}

json.dump(jsonDict, f, indent=3)
f.close()