class BTreeNode:
    #Constructor for the object (tree node)
    def __init__(self, degree, leaf=True):
        # Set at 3 for the tree
        self.degree = degree
        # Dictionary to hold words and their values
        # Syntax: "self.key[word] = confidence_score"
        self.rizzionary = {}
        # List to hold the children
        self.children = []
        #bool to check if leaf, leaf have children, if not, no children
        self.leaf = leaf

    def split_child(self, i, child):

        new_child = BTreeNode(leaf=child.leaf)
        mid = (len(child.keys) - 1) // 2
        new_key = child.keys[mid]
        new_value = child.keys[mid]
        self.keys[new_key] = new_value
        self.children.insert(i + 1, new_child)
        new_child.keys = {k: child.keys[k] for k in list(child.keys)[mid+1:]}
        child.keys = {k: child.keys[k] for k in list(child.keys)[:mid]}
        if not child.leaf:
            new_child.children = child.children[mid+1:]
            child.children = child.children[:mid+1]

    def insert_non_full(self, key, value):
        i = len(self.keys) - 1
        if self.leaf:
            self.keys[key] = value
            while i >= 0 and key < list(self.keys.keys())[i]:
                self.keys[list(self.keys.keys())[i+1]] = self.keys[list(self.keys.keys())[i]]
                i -= 1
            self.keys[list(self.keys.keys())[i+1]] = key
        else:
            while i >= 0 and key < list(self.keys.keys())[i]:
                i -= 1
            i += 1
            if len(self.children[i].keys) == self.degree:
                self.split_child(i, self.children[i])
                if key > list(self.keys.keys())[i]:
                    i += 1
            self.children[i].insert_non_full(key, value)

class BTree:
    def __init__(self, degree=3):
        self.root = BTreeNode(degree, leaf=True)

    def search(self, key):
        return self._search(key, self.root)

    def _search(self, key, node):
        if key in node.keys:
            return node.keys[key]
        elif node.leaf:
            return None
        else:
            i = 0
            while i < len(list(node.keys.keys())) and key > list(node.keys.keys())[i]:
                i += 1
            return self._search(key, node.children[i])

    def insert(self, key, value):
        if len(self.root.keys) == self.root.degree:
            new_root = BTreeNode(self.root.degree, leaf=False)
            new_root.children.append(self.root)
            new_root.split_child(0, self.root)
            self.root = new_root
        self.root.insert_non_full(key, value)
