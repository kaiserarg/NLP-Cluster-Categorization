from clustering import word2vec_clustering


thresholds = [0.9]

keywords_nums = [5,20]

for t in thresholds:
    for k in keywords_nums:
        print(t, k)
        word2vec_clustering(k, t)
