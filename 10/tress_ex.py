class TreeNode:
    """Note that we don't have to create another class in order to manipulate the nodes or the tree itself"""
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def add(self, item):
        if self.value == item:  # A binary search tree can't have two values in different vertexes
            return
        if item > self.value:
            if self.right:
                self.right.add(item)
            else:
                self.right = TreeNode(item)
        else:
            if self.left:
                self.left.add(item)
            else:
                self.left = TreeNode(item)

    def search(self, item):
        if self.value == item:  # Base case
            return True
        else:
            if item > self.value:  # Bigger than our value
                if self.right:  # Since it's a Binary tree, we move to the right son, if exists
                    return self.right.search(item)
                else:  # Bigger than all values
                    return False
            else:  # Smaller than our value
                if self.left:  # Since it's a Binary tree, we move to the left son, if exists
                    return self.left.search(item)
                else:  # Smaller than all values
                    return False


root = TreeNode(1)
root.left = TreeNode("A")
root.right = TreeNode("B")
root.left.left = TreeNode(2)
root.right.left = TreeNode(3)
root.right.right = TreeNode(4)
root.right.left.left = TreeNode("C")
# my_tree.add(2)
# my_tree.add(3)
# my_tree.add(4)
# my_tree.add(5)
# my_tree.add(0)
# my_tree.add(-1)
# my_tree.add(-2)
# my_tree.add(-3)
# print(my_tree.left.left.value)
# print(root.search(0.0))

def process_list():
    my_list = [1, 2, 3, 4, 5]
    yield from my_list
    yield my_list

# Iterate over the generator
for item in process_list():
    pass
    # print(item)


def tree_iter(root, depth):
    for i in range(depth):
        yield from tree_iter_helper(root, i)
        print(f"finished the {i} iteration")


def tree_iter_helper(root, depth):
    if depth == 0:  # Base case, we reached the prior lever to the leaves
        yield root.value  # Todo - very important! It returns a SINGLE value, of the current leaft value
        return
    if root.left:  # Left vertex exists, we check it first in order to yield the left first
        yield from tree_iter_helper(root.left, depth - 1)
        # print("From left")
    if root.right:  # Right vertex exists
        yield from tree_iter_helper(root.right, depth - 1)
        # print("From right")


i = tree_iter(root, 3)
for node in i:
    print(node)




