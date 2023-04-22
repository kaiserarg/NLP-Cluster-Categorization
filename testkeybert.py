from keybert import KeyBERT

kw_model = KeyBERT()

kw_model_multi = KeyBERT('paraphrase-multilingual-MiniLM-L12-v2')

doc = """
      Zero-shot text classification is truly a transformative piece of technology.
      These models can classify text into arbitrary categories without any fine-tuning [1]. 
      This technology provides two main benefits over traditional supervised text classification learning approaches.
      First, they make it possible to perform text classification when labelled data is non-existent, as no fine-tuning is required. 
      Next, a single model can be used to classify thousands of different labels.

      However, zero-shot text classification models are often large. 
      For example, one of the most popular zero-shot text classification models is based on the BART-large transformer architecture which has over 400 M parameters.
      This article will discuss how to use a zero-shot text classification model to produce training data and then use the generated training data to then train a smaller model that still performs well.
      As a result, this will allow NLP practitioners to train smaller models that can be more easily implemented in production by reducing hardware requirements and energy consumption.
      """

keywords = kw_model.extract_keywords(doc, top_n=10)
print(keywords)