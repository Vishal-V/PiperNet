import os

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def predict(text):
    if not os.path.exists('sentiment'):
        nltk.download('vader_lexicon', '.')
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(text)
    return {max(ss, key=ss.get): ss[max(ss, key=ss.get)]}
