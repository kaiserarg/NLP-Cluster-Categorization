import csv

def read_csv_data(file):
    youtube_list = []
    csv_file = csv.reader(file, delimiter=',')
        
    for tuple in csv_file:
        youtube_list.append((tuple[0].strip(), tuple[1]))
            
    return youtube_list

with open("yt_anskey/youtubers_tagged.csv", "r") as file:
    youtuberList = read_csv_data(file)

for x in youtuberList:
   print(x)
