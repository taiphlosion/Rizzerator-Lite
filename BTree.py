import pandas as pd
import math
from itertools import chain
import random

#Everything up until work_val is to organize the dataset to make it easier for the tree
# main master sheet
# mast = pd.read_csv('FinalDictionary.csv')
# mast['Score'] = mast['Score'].apply(lambda x: math.floor(x * 10) / 10)
# mast.to_csv('FinalDic_Round.csv')

# #sort all score values from lowest to highest
# mast = mast.sort_values(by=['Score'])
# mast.to_csv('FinalDic_Ordered.csv')

# #round all scores values down to just 1 decimal place and rounds down like 4.99 would be rounded down to 4.9
# #note that this is not ordered
# mast['Score'] = mast['Score'].apply(lambda x: math.floor(x * 10) / 10)
# mast.to_csv('FinalDic_Round_Ordered.csv')

#Finalized and ordered dataset
work_val = pd.read_csv('FinalDic_Round_Ordered.csv')


class Node:
    def __init__(self, t, is_leaf=True):
        self.t = t  # the minimum degree of the node
        self.keys = []  # a list of keys (confidence score values) For the purpose of this project, it just needs to hold one
        self.words = []  # a list of associated words for each key
        self.children = []  # a list of child nodes
        self.is_leaf = is_leaf #Bool to check if node is a leaf

    #Uses recursion search to find the node with the the desired confidence value like (4.7)
    def search(self, key):
        i = 0
        while i < len(self.keys) and key > self.keys[i]:
            i += 1
        if i < len(self.keys) and key == self.keys[i]:
            return self.words[i]
        elif self.is_leaf:
            return None
        else:
            return self.children[i].search(key)

    #Detects if node is full and then split accordingly if it passes limit size
    #also makes sure that its list and keys are transferred over appropriately
    def split_child(self, i, child):
        new_child = Node(self.t, is_leaf=child.is_leaf)
        mid = self.t - 1
        new_key = child.keys[mid]
        new_words = child.words[mid:]

        self.keys.insert(i, new_key)
        self.words.insert(i, new_words)
        self.children.insert(i + 1, new_child)

        new_child.keys = child.keys[mid+1:]
        new_child.words = child.words[mid+1:]

        child.keys = child.keys[:mid]
        child.words = child.words[:mid]

        if not child.is_leaf:
            new_child.children = child.children[mid+1:]
            child.children = child.children[:mid+1]


class BTree:
    #Tree object, with t being the degree of the tree
    def __init__(self, t):
        self.root = Node(t, is_leaf=True)
        self.t = t

    #Takes the key(confidence value) and returns node if it has that value, if not return None
    def search(self, key):
        return self.root.search(key)

    #Inserts node into the tree, and if full, split into child nodes and makes new root
    #Uses the other insert function to traverse tree to find right place to insert tree
    def insert(self, key, words):
        if len(self.root.keys) == 2*self.t - 1:
            new_root = Node(self.t, is_leaf=False)
            new_root.children.append(self.root)
            new_root.split_child(0, self.root)
            self.root = new_root
        self._insert_non_full(self.root, key, words)

    #Recursively traverses tree to find right location to insert into the new tree.
    def _insert_non_full(self, node, key, words):
        i = len(node.keys) - 1
        #Inserts if node is a leaf, meaning it's in the right place
        if node.is_leaf:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            node.keys.insert(i+1, key)
            node.words.insert(i+1, words)
        #If its an internal node, find the appropriate child node to continue the recursive insert process
        #Also checks if child node is full and splits accordingly
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2*self.t - 1:
                node.split_child(i, node.children[i])
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, words)

#A dictionary to hold the list of words that is associated with the key (confidence value)

con_val = {}

#Function push all values from the data set into a dictionary to later be inserted into the tree
def word_number_org():
    for index, row in work_val.iterrows():
        score = row['Score']
        word = row['Word']
        if score not in con_val:
            con_val[score] = []
        con_val[score].append(word)


#Some nodes have a list inside a list, this is to help remedy this and make it just a normal list
#Makes it possible to sort and traverse the tree
def flatten_list(lst):
    if isinstance(lst, list) and any(isinstance(elem, list) for elem in lst):
        return list(chain.from_iterable(lst))
    else:
        return lst


#Function to return the top 10 words of the score of a node (Like the top 10 most confident words with a score of 4.7)
def top_10(lst):
    last_ten = lst[-10:]
    return last_ten


#Function to return the bottom 10 words of the score of a node (Like the top 10 most unconfident words with a score of 4.7)
def bottom_10(lst):
    bottom_10 = lst[:10]
    return bottom_10


#Function to return the random 10 words of the score of a node (Like the 10 random words with a score of 4.7)
def random_10(lst):
    random_10 = random.sample(lst, 10)
    return random_10


#Searches through each node of the tree and checks the list of words of each node, using function of the tree
def search_word(word_search):
    found = False
    for i in range(10, 51):
        j = i/10
        list = tree.search(j)
        if (not found):
            for word in list:
                if word == word_search:
                    found = True
                    return
        if (j == 5.0):
            return

#Function to get all data ready to be inserted into the tree
word_number_org()

# Create a new tree
# Must set tree to degree 21 to work properly, if not some nodes might have overlapping words from different scores. 
tree = BTree(21)

#Inserts all values into the tree
for i in range(10, 51):
    j = i/10
    tree.insert(j, con_val[j])

# In main, use this function to search for word in the tree
search_word("bastille")

# Values are from the user. Current one is default
k = 4.7
# For main, use everything inside the print statement for the main, if you want a list of words associated with the score
# Words with scores closest to the k value (ascending order), making it the least confident for that bucket (4.7)
print(bottom_10(flatten_list(tree.search(k))))
# 10 words with scores fartest from the k value (ascending order), making it the most confident for that bucket (4.7)
print(top_10(flatten_list(tree.search(k))))
# Random words with scores in that bucket (4.7) (no specific order), generates a list of 10
print(random_10(flatten_list(tree.search(k))))
