# import preProccess as pre

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


# Create a new tree
tree = BTree(3)


    


tree.insert(1.5, "apple")
tree.insert(1.5, "apples")
tree.insert(1.5, "appless")
tree.insert(1.5, "applessss")

tree.insert(1.7, "banana")
tree.insert(1.8, "sex")
tree.insert(1.8, ["grape", "trees", "glass", "dirt"])

tree.insert(1.9, "kiwi")

print ("\n")
print ("\n")
print (tree.search(1.8))

# Search for a key
# result = tree.search(0.8)
# print(result)  # Output: ['pear', 'grape']

# # Search for a deleted key
# result = tree.search(0.5)
# print(result)  # Output: None
