import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import json
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity


def keyword_similarity(k1, k2, model):
    try:
        vec1 = model.get_vector(k1)
    except KeyError:
        return 0
    try:
        vec2 = model.get_vector(k2)
    except KeyError:
        return 0

    return cosine_similarity(vec1.reshape(1, -1), vec2.reshape(1, -1))[0][0]

def normalize(lst):
    max_val = max(lst)
    min_val = min(lst)

    if max_val == min_val:
        return [0.0 for _ in lst]

    return [(x - min_val) / (max_val - min_val) for x in lst]

def weighted_cosine_similarity(k_lst1, k_lst2, model, threshold):
    sim_scores = []

    for k1 in k_lst1:
        for k2 in k_lst2:
            sim = keyword_similarity(k1[0], k2[0], model)
            if sim >= threshold:
                sim_scores.append((sim, k1[1], k2[1]))

    if not sim_scores:
        return 0

    score = 0
    for sim, k1_score, k2_score in sim_scores:
        score += sim * k1_score * k2_score

    # Normalize the scores
    normalized_scores = normalize([s[0] for s in sim_scores])
    normalized_weighted_sum = sum([s * k1 * k2 for s, k1, k2 in zip(normalized_scores, [s[1] for s in sim_scores], [s[2] for s in sim_scores])])

    return normalized_weighted_sum / len(sim_scores)

def word2vec_clustering(keyword_num, threshold):
    # load Word2Vec model & get the keywords & scores
    word2vec_model = KeyedVectors.load_word2vec_format("GoogleNews-vectors-negative300.bin.gz", binary=True, limit=500000)
    with open("keywords.json", "r") as file:
        keyword_data = json.load(file)

    keyword_data = {youtuber: keywords[:keyword_num] for youtuber, keywords in keyword_data.items()}
    data = {
        "youtuber": [],  # YouTuber
        "keywords": [],  # keywords & their weights
    }
    for channel, keywords in keyword_data.items():
        data["youtuber"].append(channel)
        data["keywords"].append([(k[0], k[1]) for k in keywords])

    df = pd.DataFrame(data)
    word2vec_graph = nx.Graph()

    # nodes: YouTubers
    # edges: similarity scores
    max_score = 0
    scores = []
    for index1, row1 in df.iterrows():
        word2vec_graph.add_node(row1["youtuber"])
        for index2, row2 in df.iterrows():
            if index1 < index2:
                score = weighted_cosine_similarity(row1["keywords"], row2["keywords"], word2vec_model, threshold)
                if score > 0:
                    scores.append(score)
                    max_score = max(max_score, score)
                    word2vec_graph.add_edge(row1["youtuber"], row2["youtuber"], weight=score)

    # Normalize the edge weights to a range of 0 to 1
    for u, v, d in word2vec_graph.edges(data=True):
        d['weight'] /= max_score

    # output the graph
    positions = nx.kamada_kawai_layout(word2vec_graph)
    plt.figure(figsize=(10, 10))
    nx.draw(word2vec_graph, positions, node_color='lightblue', with_labels=True, node_size=1500, font_size=12)
    labels = nx.get_edge_attributes(word2vec_graph, 'weight')
    nx.draw_networkx_edge_labels(word2vec_graph, positions, edge_labels=labels)
    nx.write_gexf(word2vec_graph, "word2vec_graphs/graph_" + str(keyword_num) + "_" + str(threshold) + ".gexf")