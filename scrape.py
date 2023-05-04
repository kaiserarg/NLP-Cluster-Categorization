from youtube_transcript_api import YouTubeTranscriptApi as transcriptAPI
from youtube_transcript_api.formatters import TextFormatter
import scrapetube
import json
from yt_anskey.youtuberlist import youtuberList

formatter = TextFormatter()

youtubeURL = "https://www.youtube.com/@"

f = open("transcript_raw.json", "a")

jsonDict = {}

for i in range(len(youtuberList)):
    try:
        videos = scrapetube.get_channel(None, youtuberList[i][1], 10, 1, "popular")
        corpus = ""
        for video in videos:
            transcriptList = transcriptAPI.get_transcript(video['videoId'])
            corpus = corpus + formatter.format_transcript(transcriptList, languages=['en', 'en-US']).replace("\n", " ")
            jsonDict[youtuberList[i][0]] = {"name": youtuberList[i][0], "corpus": corpus}
    except Exception as e:
        print("error is" + youtuberList[i][1])
        continue
    
    print(i)

json.dump(jsonDict, f, indent=3)
f.close()