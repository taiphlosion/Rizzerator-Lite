import requests
import pandas as pd
import random
import re
import contractions
import csv
#import stopwords 
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords


# Create personalized list of stop words
stop_words = [ "of", "should", "not", "are", "i", "her", "here", "their", "again", "can", "above", "these", "will", "all", 
            "them", "has", "she", "him", "his", "itself", "it", "is", "out", "had", "he", "hers", "because", "were", "than", "not",
            "and", "under", "during", "into", "am", "have", "yours", "a", "some", "have", "has", "ours", "or", "by", "our", "at",
            "on", "same", "you", "does", "was", "did", "theirs", "herself", "himself",
            "does", "they", "up", "between", "such", "both", "nor", "having", "are", "an", "no", "ain't", "as", "before", "with",
            "have", "other", "she", "in", "for", "themselves", "do", "the", "against", "so", "ourselves", "to", "did",
            "doing", "each", "been", "has", "after", "off", "but", "through", "it", "this", "own",
            "any", "now", "if", "while", "down", "only", "being", "my", "had", "we", "then", "until", "from",
            "further", "there", "that", "went", "those"]

word_scores = {}

for word in set(stop_words):
    word_scores[word] = 3
    

# Read in the csv file
df = pd.read_csv('SentenceCorpus.csv')


# Define a function to preprocess each sentence
def preprocess_sentence(sentence):
    # Convert the sentence to lowercase
    sentence = str(sentence).lower()
    
    # Remove words containing numbers from the sentence
    sentence = re.sub(r'\b\w*\d\w*\b', '', sentence)
    
    # Break apart contractions using the contractions library
    sentence = contractions.fix(sentence)
    
    # Remove all non-alphabetic characters from the sentence
    sentence = re.sub(r'[^a-zA-Z\s]', '', sentence)
    
    # Ensure the sentence is returned as a string of words
    sentence = ' '.join(sentence.split())
    
    return sentence

# Preprocess each sentence in the 'Sentence' column
df['Sentence'] = df['Sentence'].apply(preprocess_sentence)

# Print the updated dataframe
# print(df.head())

# Define a function to tokenize a sentence and return a list of words
def tokenize(sentence):
    return sentence.split()

# Update the word_scores dictionary with words and their scores
for index, row in df.iterrows():
    sentence = row['Sentence']
    score = row['Score']
    words = tokenize(sentence)

    for word in words:
        if word not in stop_words:
            if word not in word_scores:
                word_scores[word] = [score]
            else:
                word_scores[word].append(score)

# Calculate the average score for each word
word_final_scores = {}
for word, scores in word_scores.items():
    if isinstance(scores, list):
        word_final_scores[word] = sum(scores) / len(scores)
    else:
        word_final_scores[word] = scores


# Print the count of all words in the dictionary
# print(f"Total words in the dictionary: {len(word_final_scores)}")

# Print 10 random words in the dictionary with their associated scores
random_words = random.sample(list(word_final_scores.items()), 10)
for word, score in random_words:
    print(f"{word}: {score}")