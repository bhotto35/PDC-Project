import pandas as pd
import numpy as np
from flair.models import TextClassifier
from flair.data import Sentence
sia = TextClassifier.load('en-sentiment')
def single_flair_prediction(x):
    sentence = Sentence(x)
    sia.predict(sentence)
    #print("sentence"+x, sentence.labels)
    score = sentence.labels[0]
    if "POSITIVE" in str(score):
        return "pos"
    elif "NEGATIVE" in str(score):
        return "neg"
    else:
        return "neu"    
def parallel_flair_sentiment(iterable):
    
    if iterable.ndim==1:
        sentiment = single_flair_prediction(iterable[3])
        return np.append(iterable,sentiment)
    else:
        sentiment_arr = list()
        n = len(iterable)
        for i in range(n):
            sentiment = single_flair_prediction(iterable[i][3])
            #print("arr: ",sentiment_arr,"sentiment:",sentiment)
            sentiment_arr.append(sentiment)
        newdf = pd.DataFrame(iterable,columns=['date','ticker','headline'])
        newdf['sentiment'] = sentiment_arr
        return newdf
