#poop butt fart
import pandas as pd
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

words = pd.read('unigram_freq.csv')
words['']