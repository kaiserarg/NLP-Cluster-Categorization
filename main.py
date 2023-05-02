from clustering import word2vec_clustering


thresholds = [0.6, 0.7, 0.8, 0.9]

keywords_nums = [5,10,15,20]

for t in thresholds:
    for k in keywords_nums:
        print(t, k)
        word2vec_clustering(k, t)
