import pandas as pd
import math
from itertools import chain
import random

#main master sheet
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

work_val = pd.read_csv('FinalDic_Round_Ordered.csv')

class Node:
    def __init__(self, t, is_leaf=True):
        self.t = t  # the minimum degree of the node
        self.keys = []  # a list of keys (confidence score values)
        self.words = []  # a list of associated words for each key
        self.children = []  # a list of child nodes
        self.is_leaf = is_leaf

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
    def __init__(self, t):
        self.root = Node(t, is_leaf=True)
        self.t = t

    def search(self, key):
        return self.root.search(key)

    def insert(self, key, words):
        if len(self.root.keys) == 2*self.t - 1:
            new_root = Node(self.t, is_leaf=False)
            new_root.children.append(self.root)
            new_root.split_child(0, self.root)
            self.root = new_root
        self._insert_non_full(self.root, key, words)

    def _insert_non_full(self, node, key, words):
        i = len(node.keys) - 1
        if node.is_leaf:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            node.keys.insert(i+1, key)
            node.words.insert(i+1, words)
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2*self.t - 1:
                node.split_child(i, node.children[i])
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, words)

con_val = {}

def word_number_org():
    for index, row in work_val.iterrows():
        score = row['Score']
        word = row['Word']
        if score not in con_val:
            con_val[score] = []
        con_val[score].append(word)

def flatten_list(lst):
    if isinstance(lst, list) and any(isinstance(elem, list) for elem in lst):
        return list(chain.from_iterable(lst))
    else:
        return lst

def top_10(lst):
    print ("Top 10:", end ="\n")
    last_ten = lst[-10:]
    return last_ten

def bottom_10(lst):
    print ("Bottom 10:", end="\n")
    bottom_10 = lst[:10]
    return bottom_10

def random_10(lst):
    print ("Random 10:", end="\n")
    random_10 = random.sample(lst, 10)
    return random_10

word_number_org()

# Create a new tree
# Must set tree to degree 21 to work properly
tree = BTree(21)

for i in range(10, 51):
    j = i/10
    tree.insert(j, con_val[j])

for i in range(10, 51):
    k = i/10
    print (k, end=":\n")
    print(bottom_10(flatten_list(tree.search(k))))
    print(top_10(flatten_list(tree.search(k))))
    print(random_10(flatten_list(tree.search(k))))
    print ("\n")

