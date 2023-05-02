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
    # normalization = 0
    for sim, k1_score, k2_score in sim_scores:
        score += sim * k1_score * k2_score
        # normalization += k1_score * k2_score

    return score/len(sim_scores)
    # return score/normalization


def word2vec_clustering(keyword_num, threshold):
    # load Word2Vec model & get the keywords & scores
    word2vec_model = KeyedVectors.load_word2vec_format("GoogleNews-vectors-negative300.bin.gz", binary=True, limit=500000)
    with open("keywords.json", "r") as file:
        keyword_data = json.load(file)


    keyword_data = {}
    for channel, keywords in keyword_data.items():
        keyword_data[channel] = keywords[:keyword_num]
    data = {
        "YouTuber": [], #YouTuber
        "Keywords": [], #keywords & their weights
    }
    for channel, keywords in keyword_data.items():
        data["youtuber"].append(channel)
        data["keywords"].append([(k[0], k[1]) for k in keywords])


    df = pd.DataFrame(data)
    word2vec_graph = nx.Graph()

    # nodes: YouTubers 
    # edges: similarity scores
    for index1, row1 in df.iterrows():
        word2vec_graph.add_node(row1["youtuber"])
        for index2, row2 in df.iterrows():
            if index1 < index2:
                score = weighted_cosine_similarity(row1["keywords"], row2["keywords"], word2vec_model, threshold)
                if score > 0:
                    word2vec_graph.add_edge(row1["youtuber"], row2["youtuber"], weight=score)

    # output the graph
    positions = nx.kamada_kawai_layout(word2vec_graph)
    plt.figure(figsize=(10, 10))
    nx.draw(word2vec_graph, positions, node_color='lightblue', with_labels=True, node_size=1500, font_size=12)
    labels = nx.get_edge_attributes(word2vec_graph, 'weight')
    nx.draw_networkx_edge_labels(word2vec_graph, positions, edge_labels=labels)
    nx.write_gexf(word2vec_graph, "word2vec_graphs/graph_"+keyword_num+"_"+threshold+".gexf")
