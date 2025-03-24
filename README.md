# For the Best Viewing Experience
Please read the PDF here: [A_Clustering_System_For_YouTube_Channel_Classification.pdf](https://github.com/kaiserarg/NLP-Cluster-Categorization/blob/main/A_Clustering_System_For_YouTube_Channel_Classification.pdf)

---

# A Clustering System For YouTube Channel Classification

**Bradley Huang**  
*brad.huang@nyu.edu*  
**Shenyi Huang**  
*sh6210@nyu.edu*  
**Deniz Qian**  
*dq2024@nyu.edu*  
**Daniel Ni**  
*dn2212@nyu.edu*  

Date: May 2, 2023

---

## Abstract

In this paper, we propose an unsupervised YouTube channel classification system based on the content of the channels. We extract different numbers of keywords and their weights from the video scripts of 225 channels and use the Word2Vec technique to generate embeddings for each keyword. We generate clusters with the similarity scores between all channels with different threshold values. We conduct quantitative analysis and qualitative analysis based on a manually tagged label baseline system and a predefined YouTube label baseline system. Finally, our analysis shows that our system has the best performance when more keywords are used for each channel and a lower threshold value is applied when calculating the similarity score.

---

## 1. Introduction

Online video sharing and streaming platforms have become a large part of the 21st century. YouTube, being one of the leading platforms, has grown exponentially since its initial launch in 2005. The platform is home to millions of channels that produce content covering a wide array of categories. As the platform continues to grow, users often struggle to find channels that align with their interests due to a massive amount of videos covering various topics. Upon creation of a new YouTube channel, content creators are tasked with choosing one of 15 categories to describe the type of content they will publish. However, many of them steer away from this initial choice. This causes their newer videos to be filtered into incorrect categories on third-party platforms that users use to search for new content creators. This problem calls for an efficient and scalable solution to categorize YouTube channels in order to improve user experience with regard to content discovery. 

In this project, we developed a system to cluster similar YouTube channels based on a channel’s most popular videos’ transcripts. By organizing the channels into clusters, our project enables users to avoid surfing through millions of channels to find content, but rather can observe a cluster that suits their interests and find new content creators from it.

Our primary contributions are as follows:

1. We describe a general framework for our YouTube channel categorization that relies on multiple methodologies and implementations (see Section 3).  
2. We assess the quality of our clusters by providing a qualitative analysis of our final graphs, comparing different graphs that were created using different numbers of keywords and different thresholds of word similarity.  
3. We also assess the quality of our clusters by providing a quantitative analysis using different metrics such as modularity and F-score, which are calculated by comparing the channels in the clusters created by our system to the predefined data set and a manually tagged data set.

The paper is organized as follows. In Section 2, we introduce related work pertaining to content-based classification and clustering techniques. In Section 3, we describe in detail our methods and implementations for YouTube channel categorization. In Section 4, we describe an evaluation of our results, including both a quantitative and qualitative analysis. In Section 5, we draw final conclusions and discuss future work.

---

## 2. Related Work

Manual keyword extraction is highly cumbersome, and there is much research in developing unsupervised keyword extraction from texts. Unsupervised methods can be categorized into graph-based, statistic-based, and topic-based methods \[1\]. Within topic-based KPE methods, there are clustering-based methods where candidate keyphrases extracted from text are agglomerated and used as vertices in a complete graph and given a significance score with a graph-based ranking model \[2\]. Finally, key phrases are then selected from candidates in top-ranked topics and returned.

KeyBERT utilizes an unsupervised KPE model called Masked Document Embedding Rank, which employs a novel method of “masking” keywords in a masked version of the original document and looking for the least semantically similar sections to pick out keywords \[1\]. The logic here is that the most important keywords are unique and thus should nearly completely define the meaning of sentence structures in the document, meaning that their removal should cause the greatest discrepancies in semantic similarities when comparing the masked document and the original document.

TextRank is a graph-based model which applies an adapted version of Google’s PageRank algorithm \[3\] iteratively on a graphical representation of the input text to rank and extract keywords, similarly to how PageRank ranks the relevance of websites. TextRank introduces the idea of “recommendation,” where the importance of words in a text is identified not only through the local context of a single graph unit but also by recursively computing recommendations given by other related text units in the graph, and then finally computing an importance score based on how important its related words are.

---

## 3. Methods and Implementation

Below we detail six methods that accomplish our goal of clustering YouTube channels based on their content:

1. **Data Selection**  
2. **Data Scraping**  
3. **Keyword Extraction**  
4. **Similarity Score Calculation**  
5. **Clustering Technique**  
6. **Modularity**

### 3.1 Baseline Systems and Data Selection

To evaluate our system, we created two baseline systems to compare our final clusters to:

- The categories defined by YouTube upon channel creation (“predefined” categories).  
- A set of categories we annotated ourselves based on channel content (“manually tagged”).

**Predefined Baseline**:  
A list of 15 YouTube channels from each of the 15 predefined YouTube categories, totaling 225 channels:

- Autos & Vehicles  
- Comedy  
- Education  
- Entertainment  
- Film and Animation  
- Gaming  
- Howto & Style  
- Music  
- News & Politics  
- Nonprofits & Activism  
- People & Blogs  
- Pets & Animals  
- Science & Technology  
- Sports  
- Travel & Events  

We excluded channels lacking transcripts or that were not primarily English. We used Social Blade to rank the most subscribed YouTube channels per category and compiled the top channels into a dataset of 225 YouTubers, each with a link and a predefined label.

**Manually Tagged Baseline**:  
Using the same 225 channels, four annotators manually categorized each into one of 18 categories: Cars, Variety Entertainment, Comedy, Technology, Food, Education, Kids, Beauty, Film, Gaming, Howto, Music, News, Politics, Religion, Animals, Sports, and Travel.

### 3.2 Data Scraping

Our goal was to scrape the transcripts of each channel’s top 10 most-viewed English-transcript videos:

1. We used `scrapetube` to find the top 10 video IDs for each of the 225 channels.  
2. We then used the **YouTube Transcript/Subtitle API** to retrieve each video’s transcript.  
3. We formatted and stored these transcripts into a corpus.  

We merged these 10 transcripts to create one corpus per channel, then wrote each YouTuber’s name and corpus to a JSON file for subsequent processing.

### 3.3 Keyword Extraction

We used **KeyBERT** to extract keywords from each channel’s corpus. KeyBERT is based on **BERT** \[4\], which provides powerful word embeddings. KeyBERT calculates cosine similarities to find the most relevant terms or keyphrases to the channel’s overall content.

For every channel’s corpus, we extracted **5, 10, 15, and 20 keywords**. Each keyword has an associated **weight** that indicates how representative it is of the corpus.

### 3.4 Similarity Score Calculation

#### 3.4.1 Word2Vec

To obtain vector representations of each keyword, we used **Word2Vec** \[5\]. Specifically, we loaded a pre-trained model from **gensim** that was trained on Google News (300-dimensional embeddings).

#### 3.4.2 Weighted Cosine Similarity Score

To measure similarity between two channels, we define a **Weighted Cosine Similarity (WCS)**. First, we compute **cosine similarity** between all keyword pairs whose embeddings exceed a threshold.

**Cosine similarity** of two vectors \(A\) and \(B\):

$$
\mathrm{cos\_sim}(A, B) = \frac{\sum_{i=1}^{n} A_i \,B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \,\sqrt{\sum_{i=1}^{n} B_i^2}}
$$

We only consider \(\mathrm{cos\_sim}(A, B)\) if it meets one of four thresholds: **0.6, 0.7, 0.8, or 0.9**.

Each keyword is assigned a KeyBERT-derived weight (\(w\)). Once a keyword pair \((i, j)\) meets the threshold, its Weighted Cosine Similarity is:

$$
\mathrm{WCS}_{i,j} 
\,=\, \left(\frac{\mathrm{cos\_sim}_{i,j} \;-\; \min(\mathrm{cos\_sim})}{\max(\mathrm{cos\_sim}) - \min(\mathrm{cos\_sim})}\right) \;\cdot w_i \;\cdot w_j
$$

where:
- \(\mathrm{cos\_sim}_{i,j}\) is the cosine similarity of keyword \(i\) (channel 1) and keyword \(j\) (channel 2).  
- \(w_i\) and \(w_j\) are the KeyBERT keyword weights.  
- \(\max(\mathrm{cos\_sim})\) and \(\min(\mathrm{cos\_sim})\) are the maximum and minimum similarity values among all pairs that exceed the threshold.  
- If \(\max(\mathrm{cos\_sim}) = \min(\mathrm{cos\_sim})\) or if \(\mathrm{cos\_sim}_{i,j}\) is below threshold, then \(\mathrm{WCS}_{i,j} = 0.\)

Finally, the overall **channel-to-channel similarity** is:

$$
\mathrm{Total\_WCS} \;=\; \frac{1}{N}\; \sum_{i=1}^{n} \sum_{j=1}^{m} \mathrm{WCS}_{i,j}
$$

where \(N\) is the number of non-zero \(\mathrm{WCS}_{i,j}\) values across all keyword pairs from both channels.

### 3.5 Graphs

Using **NetworkX**, we build a graph where each node represents a **YouTuber**, and each edge’s weight is the **Total_WCS** between two channels.

### 3.6 Clustering Technique and Modularity

We apply the `greedy_modularity_communities` method \[6\], which performs Clauset-Newman-Moore greedy modularity maximization. This returns a set of communities (clusters) based on the edge weights in our graph.

We also compute a **modularity score**, indicating how well the clusters are separated internally and externally. A higher modularity implies more distinct communities, but it does not necessarily correlate with higher accuracy in matching our baseline labels.

---

## 4. Evaluation and Results

### 4.1 F-score Evaluation Method

We employ a **greedy** cluster matching approach for precision, recall, and F-score:

1. For each cluster in our system’s output, find the cluster in the baseline (predefined or manually tagged) that yields the greatest overlap.  
2. Count:
   - **True Positives (\(\mathrm{TP}\))**: Channels in both clusters.  
   - **False Positives (\(\mathrm{FP}\))**: Channels in our cluster but not the baseline cluster.  
   - **False Negatives (\(\mathrm{FN}\))**: Channels in the baseline cluster but not in ours.

Let \(\sum \mathrm{TP}, \sum \mathrm{FP}, \sum \mathrm{FN}\) be the totals after summing each pair of matched clusters. Then:

$$
\mathrm{Precision} 
= \frac{\sum \mathrm{TP}}{\sum \mathrm{TP} \;+\; \sum \mathrm{FP}}
$$

$$
\mathrm{Recall} 
= \frac{\sum \mathrm{TP}}{\sum \mathrm{TP} \;+\; \sum \mathrm{FN}}
$$

$$
F\text{-score} 
= \frac{2 \,\times\, \mathrm{Precision} \,\times\, \mathrm{Recall}}{\mathrm{Precision} + \mathrm{Recall}}
$$

### 4.2 Quantitative Analysis

#### Comparison with Manually Tagged Baseline

| Threshold | 5 Keywords | 10 Keywords | 15 Keywords | 20 Keywords |
|-----------|-----------|------------|-------------|------------|
| **0.6**   | 0.312     | 0.397      | 0.460       | **0.465**   |
| **0.7**   | 0.243     | 0.370      | 0.392       | 0.432       |
| **0.8**   | 0.246     | 0.346      | 0.374       | 0.442       |
| **0.9**   | 0.216     | 0.326      | 0.355       | 0.387       |

- **Highest F-score**: 0.465 (Threshold=0.6, 20 keywords)  
- **Lowest F-score**: 0.216 (Threshold=0.9, 5 keywords)

#### Comparison with Predefined Baseline

| Threshold | 5 Keywords | 10 Keywords | 15 Keywords | 20 Keywords |
|-----------|-----------|------------|-------------|------------|
| **0.6**   | 0.287     | 0.352      | 0.417       | **0.423**   |
| **0.7**   | 0.210     | 0.329      | 0.347       | 0.394       |
| **0.8**   | 0.206     | 0.305      | 0.341       | 0.396       |
| **0.9**   | 0.182     | 0.294      | 0.322       | 0.341       |

- **Highest F-score**: 0.423 (Threshold=0.6, 20 keywords)  
- **Lowest F-score**: 0.182 (Threshold=0.9, 5 keywords)

On average, performance is **12.498% higher** when compared to the manually tagged baseline vs. the predefined baseline, likely because the original category chosen by the YouTuber may no longer represent the channel’s core content.

**Observations**:
1. **More Keywords** → Higher F-scores. Possibly because a larger keyword set covers the channel’s topics more broadly.  
2. **Lower Threshold** → Higher F-scores. Likely because more edges form in the graph, capturing partial similarities.

However, **high threshold** graphs often have higher modularity, meaning more well-separated clusters but lower overall accuracy to external labels.

### 4.3 Qualitative Analysis

We examined the final graphs in **Gephi**:

1. With only **5 keywords** (threshold=0.6), many YouTubers remain isolated.  
2. At **20 keywords** (threshold=0.6), we see fewer isolated channels and more dense connections.  
3. At **higher thresholds** (0.8 or 0.9), communities are more distinct but many channels end up with few or no edges.

**Selected Example Clusters (20 Keywords, 0.6 Threshold)**:

- **Food Cluster**: Channels revolve around cooking, reviews, challenges, etc. Some outliers appear due to popular food-related challenges.  
- **Vehicles/Engineering Cluster**: Channels building or modifying cars or working on engineering projects.  
- **Vague Clusters**: Channels with religion, politics, or education occasionally end up together because they share some overlapping keywords.

Overall, thematically coherent clusters are common, but channels with varied or “trending” topics can end up in less obvious groupings. Adding more channel data or refining similarity could improve this.

---

## 5. Conclusions and Future Work

We presented a model for clustering YouTube channels by analyzing transcripts of their top videos. From our analysis:

- **More keywords** and **lower threshold** generally improve cluster accuracy (F-scores up to 0.465).  
- **High threshold** or **fewer keywords** yield less overlap among channels but can produce higher modularity (tighter clusters).

Because F-scores remain under 0.5, there is substantial room for improvement.

### Future Directions

1. **Alternative Embeddings**: Compare Word2Vec to GloVe, or investigate context-sensitive embeddings like BERT or GPT-based embeddings (though the latter may require system changes).  
2. **Hyperparameter Tuning**: Explore additional thresholds or a larger range of keyword counts to see if performance peaks.  
3. **Runtime Optimization**: Our approach can be slow; faster implementations will allow for deeper parameter searches.  
4. **Additional Data Scraping**: Scraping more (or more recent) videos per channel might more accurately capture a channel’s evolving content.

---

## References

1. Zhang, Y. et al. 2023. "MDERank: A Masked Document Embedding Rank Approach for Keyphrase Extraction." arXiv preprint.  
2. Bougouin, A., Boudin, F., and Daille, B. 2013. "TopicRank: Graph-Based Topic Ranking for Keyphrase Extraction." *International Joint Conference on Natural Language Processing*.  
3. Brin, S. and Page, L. 1998. "The Anatomy of a Large-Scale Hypertextual Web Search Engine." *Computer Networks and ISDN Systems*.  
4. Devlin, J., Chang, M.W., Lee, K., and Toutanova, K. 2019. "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding." *NAACL-HLT*.  
5. Mikolov, T., Chen, K., Corrado, G., and Dean, J. 2013. "Efficient Estimation of Word Representations in Vector Space." *ICLR*.  
6. Clauset, A., Newman, M.E.J., and Moore, C. 2004. "Finding Community Structure in Very Large Networks." *Physical Review E 70, 066111*.

---

## Appendix

### GitHub Repository Link

[https://github.com/kaiserarg/NLP-Cluster-Categorization](https://github.com/kaiserarg/NLP-Cluster-Categorization)
