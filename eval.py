import os
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities, modularity
import numpy as np
import csv
import numpy as np
from scipy.optimize import linear_sum_assignment
from collections import defaultdict
import re
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import recall_score, precision_score

def read_csv_data(file):
    pre = []
    man = []
    csv_file = csv.reader(file, delimiter=',')
        
    for tuple in csv_file:
        pre.append((tuple[0].strip(), tuple[2]))
        man.append((tuple[0].strip(), tuple[3]))
            
    return pre, man

def f_score(list_a, list_b):
    categories = {}

    for name, category in list_a:
        if category not in categories:
            categories[category] = []
        categories[category].append(name)

    list_a = list(categories.values())

    tp, fp, fn = 0, 0, 0

    for cluster_a in list_a:
        max_overlap = 0
        for cluster_b in list_b:
            common_elements = len(set(cluster_a).intersection(cluster_b))
            max_overlap = max(max_overlap, common_elements)
        
        tp += max_overlap
        fn += len(cluster_a) - max_overlap
    
    for cluster_b in list_b:
        max_overlap = 0
        for cluster_a in list_a:
            common_elements = len(set(cluster_a).intersection(cluster_b))
            max_overlap = max(max_overlap, common_elements)

        fp += len(cluster_b) - max_overlap

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    
    if precision + recall == 0:
        return 0
    
    f_score = 2 * (precision * recall) / (precision + recall)

    return precision, recall, f_score

directory = 'word2vec_graphs'
files = os.listdir(directory)
index = 0

with open("yt_anskey/youtubers_tagged.csv", "r") as file:
    predefinedList, manualTaggedList = read_csv_data(file)

csv_filename = "graph_analysis_results.csv"
csv_columns = ['File', 'Keywords', 'Threshold', 'Modularity', 'Category List Precision', 'Category List Recall', 'Category List F-score',
               'Manually Tagged Category Precision', 'Manually Tagged Category Recall', 'Manually Tagged Category F-score']

with open(csv_filename, mode='w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    while index < len(files):
        filename = files[index]
        if filename.endswith('.gexf'):
            with open(os.path.join(directory, filename)) as f:
                graph = nx.read_gexf(f)
                communities = greedy_modularity_communities(graph, "weight", 1, 1, None)
                communities = [list(x) for x in communities] #converts frozen set to normal set
                precision1, recall1, fscore1 = f_score(predefinedList, communities)
                precision2, recall2, fscore2 = f_score(manualTaggedList, communities)
                match = re.search(r'graph_(\d+)_(\d+\.\d+)', filename)
                keywords = int(match.group(1))
                threshold = float(match.group(2))
                modularity_val = modularity(graph, communities, "weight")
                writer.writerow({
                        'File': filename,
                        'Keywords': keywords,
                        'Threshold': round(threshold, 3),
                        'Modularity': round(modularity_val, 3),
                        'Category List Precision': round(precision1, 3),
                        'Category List Recall': round(recall1, 3),
                        'Category List F-score': round(fscore1, 3),
                        'Manually Tagged Category Precision': round(precision2, 3),
                        'Manually Tagged Category Recall': round(recall2, 3),
                        'Manually Tagged Category F-score': round(fscore2,3)
                    })
        index += 1