import csv

def read_csv_data(csv_file_name):
    list_of_tuples = []
    
    with open(csv_file_name, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        for tuple in csv_reader:
            list_of_tuples.append((tuple[0].strip(), tuple[1]))
            
    return list_of_tuples


youtuberList = read_csv_data("youtuber_list.csv")
