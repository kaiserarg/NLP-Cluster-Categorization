import math, nltk
import numpy as np
from nltk import word_tokenize

# return a dictionary of idf of each word in the corpus
def calculate_idf(docs):
    idf_dct = {}
    for i in range(len(docs)):
        docs[i] = word_tokenize(docs[i])
        for w in set(docs[i]):
            if w in idf_dct: idf_dct[w] += 1
            else: idf_dct[w] = 1
    for w in idf_dct:
        idf_dct[w] = math.log((len(docs)+1)/(idf_dct[w]+1))+1 #normalization
    return idf_dct


# return a list of dictionary that records word frequencies within a text
def calculate_tfidf(text, text_idf):
    text_tfidf = []
    for doc in text:
        text_tfidf.append({})
        for w in doc:
            if w in text_tfidf[-1]: text_tfidf[-1][w] += 1
            else: text_tfidf[-1][w] = 1    

        for w in text_tfidf[-1]: text_tfidf[-1][w] = math.log(text_tfidf[-1][w] / len(doc)) * text_idf[w] 
    return text_tfidf

def calculate_cossim(dct1, dct2):
    numer = 0
    denom_a = 0
    denom_b = 0
    for key, val in dct1.items():
        numer += val * dct2.get(key, 0.0)
        denom_a += val**2
    for key in dct1:
        denom_b += (dct2.get(key, 0.0))**2

    try:       
        return numer / math.sqrt(denom_a * denom_b)
    except ZeroDivisionError:
        return 0
    
def main():
    queries = []
    queries_idf = calculate_idf(queries)
    queries_tfidf = calculate_tfidf(queries, queries_idf)

    for i in range(len(queries_tfidf)):
        cossim_lst = []
        for j in range(i+1, len(queries_tfidf)):
            text_vector = {}
            for w in queries_tfidf[i]:
                if w in queries_tfidf[j]:
                    text_vector[w] = queries_tfidf[j][w]
                else: text_vector[w] = 0
            cossim_lst.append([i+1, j+1, calculate_cossim(queries_tfidf[i], text_vector)])
        cossim_lst.sort(key = lambda x:x[2], reverse=True)

        # for i in range(30):
        #     my_output.write(" ".join([str(ele) for ele in cossim_lst[i]])+"\n")
            

if __name__ == "__main__":
    main()