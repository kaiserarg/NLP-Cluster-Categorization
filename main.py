from clustering import word2vec_clustering


thresholds = [0.7, 0.8, 0.9, 0.95]
keywords_nums = [5,10,15,20]

for t in thresholds:
    for k in keywords_nums:
        word2vec_clustering(t, k)
