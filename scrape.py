from youtube_transcript_api import YouTubeTranscriptApi as transcriptAPI
from youtube_transcript_api.formatters import TextFormatter
import scrapetube
import json
from raw_yt_list.youtuberlist import youtuberList

formatter = TextFormatter()

youtubeURL = "https://www.youtube.com/@"

f = open("rawData.json", "a")
remaining = len(youtuberList)

jsonDict = {}

for i in range(len(youtuberList)):
    videos = scrapetube.get_channel(None, youtuberList[i][1], 10, 1, "popular")
    corpus = ""
    for video in videos:
        try:
            transcriptList = transcriptAPI.get_transcript(video['videoId'])
            corpus = corpus + formatter.format_transcript(transcriptList, languages=['en', 'en-US']).replace("\n", " ")
        except Exception as e:
            continue
    
    remaining = remaining - 1
    print(remaining)
    jsonDict[youtuberList[i][0]] = {"name": youtuberList[i][0], "corpus": corpus}
    f = open("rawData3.json", "w")
    json.dump(jsonDict, f, indent=3)

json.dump(jsonDict, f, indent=3)
f.close()