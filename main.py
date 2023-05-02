from clustering import word2vec_clustering


thresholds = [0.7]

# keywords_nums = [5,10,15,20]
keywords_nums = [10]

for t in thresholds:
    for k in keywords_nums:
        print(t, k)
        word2vec_clustering(k, t)
