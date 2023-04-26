import requests
import pandas as pd
import random
import re
import contractions
from random import uniform
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
    sentence = sentence.lower()
    
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
print(df.head())

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
# for word, score in random_words:
#     # print(f"{word}: {score}")

# # BEGIN ADDING NEW WORDS TO OUR DICTIONARY
# API_KEY = "0191a99ddfmsh88ff5e3602511e9p1bf4e8jsn6e7eb376b38d"

# # Define synonym API request
# def get_synonyms(word):
#     url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/synonyms"
#     headers = {
#         "content-type": "application/octet-stream",
#         "X-RapidAPI-Key": API_KEY,
#         "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
#     }
#     response = requests.get(url, headers=headers)
#     return response.json().get('synonyms', [])


# # Definition definition API request
# def get_definition(word):
#     url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/definitions"
#     headers = {
#         "content-type": "application/octet-stream",
#         "X-RapidAPI-Key": API_KEY,
#         "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
#     }
#     response = requests.get(url, headers=headers)
#     return response.json().get('definitions', [])


# # Import model
# from gensim.models import Word2Vec
# import gensim.downloader as api
# from gensim.models import KeyedVectors

# glove_model = api.load('glove-twitter-200')

# called_words = set()
# used_words = set()

# def k_nearest_neighbors(word, k=5, use_api=True, api_limit=50):
#     # Use the Word2Vec model to find related words
#     related_words = glove_model.most_similar(positive=[word], topn=k)
#     global api_calls, called_words

#     # Use the Words API to find synonyms if the use_api flag is set to True and the API limit is not exceeded
#     if use_api and word not in called_words and api_limit > 0 and api_calls < api_limit:
#         called_words.add(word)

#         synonyms = get_synonyms(word)
#         api_limit -= 1  # Decrement the API limit counter
#         for synonym in synonyms[:k]:
#             if synonym not in word_final_scores:
#                 api_limit -= 1  # Decrement the API limit counter
#                 definitions = get_definition(synonym)
#                 definition_score = 0
#                 word_count = 0
#                 for definition in definitions:
#                     for def_word in definition['definition'].split():
#                         if def_word in word_final_scores:
#                             definition_score += word_final_scores[def_word]
#                             word_count += 1

#                 if word_count > 0:
#                     average_definition_score = definition_score / word_count
#                     score_adjustment = uniform(-0.15, 0.15)

#                     if average_definition_score > word_final_scores[word]:
#                         new_score = min(5, word_final_scores[word] + score_adjustment)
#                     else:
#                         new_score = max(1, word_final_scores[word] + score_adjustment)

#                     word_final_scores[synonym] = new_score

#     return related_words




# # CALL OUR FUNCTIONS
# import random

# api_limit = 50
# api_calls = 0

# def random_word_k_nearest_neighbors():
#     global api_calls, used_words
#     while True:
#         # Select a random non-stop word from the dictionary
#         random_word = random.choice([word for word in word_scores.keys() if word not in stop_words and word not in used_words])
#         used_words.add(random_word)
#         print(random_word)

#         # Call k_nearest_neighbors with the random word and use_api set to True if we haven't exceeded the API limit
#         use_api = api_calls < api_limit
#         updated_words, api_calls = k_nearest_neighbors(random_word, use_api=use_api)

#         print(f"Random word: {random_word}, Updated words: {len(updated_words)}, Total API calls: {api_calls}")

#         # Break the loop if you want to stop after a certain number of iterations
#         # For example, you can stop when the used_words set reaches a certain size
#         if len(used_words) >= 80000:
#             break
        


# random_word_k_nearest_neighbors()

# # Write the updated word_final_scores to a CSV file
# import csv

# with open('word_scores.csv', 'w', newline='') as csvfile:
#     fieldnames = ['Word', 'Score']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     for word, scores in word_scores.items():
#         avg_score = sum(scores) / len(scores) if isinstance(scores, list) else scores
#         writer.writerow({'Word': word, 'Score': avg_score})
