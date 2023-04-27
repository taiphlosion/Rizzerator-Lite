class HashTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * self.capacity

    def hash(self, word):
        """
        A simple hash function that takes a word as input and returns a hash value.
        """
        hash_value = 0
        for char in word:
            hash_value += ord(char)
        return hash_value % self.capacity

    def insert(self, word, score):
        """
        Inserts a key-value pair into the hashtable.
        """
        index = self.hash(word)
        if self.buckets[index] is None:
            self.buckets[index] = []
        for pair in self.buckets[index]:
            if pair[0] == word:
                pair[1] = score
                return
        self.buckets[index].append([word, score])
        self.size += 1

    def search(self, word):
        """
        Searches for a specific key in the hashtable and returns its value.
        """
        index = self.hash(word)
        if self.buckets[index] is None:
            return None
        for pair in self.buckets[index]:
            if pair[0] == word:
                return pair[1]
        return None

    def get_top_scores(self, n=10):
        """
        Returns the n words with the highest scores in the hashtable.
        """
        scores = []
        for bucket in self.buckets:
            if bucket is None:
                continue
            for pair in bucket:
                scores.append(pair)
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:n]

    def get_top_scores_lowest(self, n=10):
        """
        Returns the n words with the highest scores in the hashtable.
        """
        scores = []
        for bucket in self.buckets:
            if bucket is None:
                continue
            for pair in bucket:
                scores.append(pair)
        scores.sort(key=lambda x: x[1], reverse=False)
        return scores[:n]
