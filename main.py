class Node:
    def __init__(self):
        self.keys = []
        self.parent = None

class Leaf(Node):
    def __init__(self):
        super().__init__()
        self.records = []
        self.next = None


class InternalNode(Node):
    def __init__(self):
        super().__init__()
        self.children = []


class BPlusTree:
    def __init__(self, order=4):
        self.root = Leaf()
        self.order = order


    def insert(self, key, value, phone):
        """
        Inserts a key-value pair into the tree. 
        It starts from the root and descends to the appropriate leaf node. 
        If the leaf node overflows, it's split.
        """
        node = self.root
        
        # Traverse down the tree until reaching a leaf node
        while isinstance(node, InternalNode):
            i = 0
            # Find the appropriate child node to descend to
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            node = node.children[i]
        
        # Find the position to insert the key in the leaf node
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        
        # If the key already exists in the leaf node, append the record
        if i < len(node.keys) and key == node.keys[i]:
            node.records[i].append((value, phone))
        else:
            # Otherwise, insert the key and record
            node.keys.insert(i, key)
            node.records.insert(i, [(value, phone)])
        
        # If the leaf node overflows, split it
        if len(node.keys) > self.order:
            self.split_leaf(node)


    def split_leaf(self, leaf):
        """
        Splits a leaf node into two when it overflows. 
        It redistributes keys and records between the original and the new leaf node.
        """
        new_leaf = Leaf()
        mid = len(leaf.keys) // 2
        
        # Move the second half of keys and records to the new leaf
        new_leaf.keys = leaf.keys[mid:]
        new_leaf.records = leaf.records[mid:]
        leaf.keys = leaf.keys[:mid]
        leaf.records = leaf.records[:mid]
        
        # Update the pointers
        if leaf.next:
            new_leaf.next = leaf.next
        leaf.next = new_leaf
        
        # Update parent reference
        new_leaf.parent = leaf.parent
        
        # Insert the first key of the new leaf into the parent
        self.insert_internal(leaf.parent, leaf, new_leaf, new_leaf.keys[0])


    def insert_internal(self, parent, left_child, right_child, key):
        """
        Inserts a new internal node between the parent and its child nodes 
        if the child node overflows after insertion.
        """
        # If the parent is None, create a new root node
        if parent is None:
            new_root = InternalNode()
            new_root.keys = [key]
            new_root.children = [left_child, right_child]
            self.root = new_root
            left_child.parent = new_root
            right_child.parent = new_root
            return
        
        # Find the position to insert the median key into the parent
        i = 0
        while i < len(parent.keys) and key > parent.keys[i]:
            i += 1
        parent.keys.insert(i, key)
        parent.children.insert(i + 1, right_child)
        right_child.parent = parent
        
        # If the parent overflows, split it
        if len(parent.keys) > self.order:
            self.split_internal(parent)


    def split_internal(self, node):
        """
        Splits an internal node into two when it overflows. 
        It redistributes keys and child nodes between the original and the new internal node.
        """
        new_node = InternalNode()
        mid = len(node.keys) // 2
        median_key = node.keys[mid]
        
        # Move the second half of keys and children to the new node
        new_node.keys = node.keys[mid + 1:]
        new_node.children = node.children[mid + 1:]
        for child in new_node.children:
            child.parent = new_node
        
        node.keys = node.keys[:mid]
        node.children = node.children[:mid + 1]
        
        # If the node is the root, create a new root
        if node == self.root:
            new_root = InternalNode()
            new_root.keys = [median_key]
            new_root.children = [node, new_node]
            self.root = new_root
            node.parent = new_root
            new_node.parent = new_root
        else:
            # Otherwise, insert the median key into the parent
            new_node.parent = node.parent
            self.insert_internal(node.parent, node, new_node, median_key)


    def search(self, key):
        """
        Searches an input name starting from the root and traversing down to 
        the leaf node based on the key. Then it searches within the leaf node 
        for the key and returns the record.
        """
        node = self.root
        
        # Traverse down the tree until reaching a leaf node
        while isinstance(node, InternalNode):
            i = 0
            # Find the appropriate child node to descend to
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]
            
        
        # Search for the key in the leaf node
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        
        # If the key is found, return it's record
        if i < len(node.keys) and key == node.keys[i]:
            return node.records[i]
    
        return None


    def print_tree(self, node=None, indent=""):
        """
        Outputs the B+Tree.
        """
        if node is None:
            node = self.root
        if isinstance(node, Leaf):
            print(indent + "Leaf: " + str(node.keys) + " " + str(node.records))
        else:
            print(indent + "Node: " + str(node.keys))
            for child in node.children:
                self.print_tree(child, indent + "  ")

# Initialise
names = ['Amelia', 'Blake', 'Caroline', 'Dominic', 'Emma', 'Fiona', 'George', 'Henry', 'Ian', 'Julia', 'Kate', 'Lola',
        'Milena', 'Nate', 'Oscar', 'Perry', 'Rachel', 'Sally', 'Travor', 'Violet', 'William', 'Yuri',
        'Zoe']
phones = ['+38' + '0' * 5 + str(index + 1) for index in range(len(names))]

tree = BPlusTree()

# Name hashing
def hash_name(name):
    """
    Converts each letter into a numeric value based 
    on its ASCII value and produces a unique hash.
    """
    name = name.lower()
    max_length = max([len(n) for n in names])
    hash_value = 0
    for i, char in enumerate(name):
        if i >= max_length:
            break
        hash_value += ord(char) ** (max_length - i - 1)

    return hash_value


for index, name in enumerate(names):
    hashed_name = hash_name(name)
    print(name, 'hash:', hashed_name)

# Insert
for index, name in enumerate(names):
    hashed_name = hash_name(name)
    tree.insert(hashed_name, name, phones[index])

print('B+TREE:')
tree.print_tree()

# Search for a name
name = 'Milena'
hashed_name = hash_name(name)
record = tree.search(hashed_name)

if record is not None:
    for i in record:
        print(f'Name {i[0]} found. Phone: {i[1]}')
else:
    print(f'Name {name} is not found')
