# Binary Search Tree: also called an ordered or sorted binary tree,
# is a rooted binary tree data structure with the key of each internal node being greater than all
# the keys in the respective node’s left subtree and less than the ones in its right subtree

class BSTNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.value)


#           1
#       2       3
#   4       5   10

A = BSTNode(1)
B = BSTNode(2)
C = BSTNode(3)
D = BSTNode(4)
E = BSTNode(5)
F = BSTNode(10)

A.left = B
A.right = C
B.left = D
B.right = E
C.left = F

print(A) # 1

# Recursive Pre Order Traversal (DFS)
# Time: O(n), Space O(n)

def pre_order(node):
    if not node:
        return

    print(node)

    pre_order(node.left)
    pre_order(node.right)

print()
print(pre_order(A)) # 1 2 4 5 3 10

# Recursive In Order Traversal (DFS)
# Time: O(n), Space O(n)

def in_order(node):
    if not node:
        return

    in_order(node.left)
    print(node)
    in_order(node.right)

print()
print(in_order(A)) # 4 2 5 1 10 3

# Recursive Post Order Traversal (DFS)
# Time: O(n), Space O(n)

def post_order(node):
    if not node:
        return

    post_order(node.left)
    post_order(node.right)
    print(node)

print()
print(post_order(A)) # 4 5 2 10 3 1

# Iterative Pre Order Traversal (DFS)
# Time: O(n), Space O(n)

def pre_order_iterative(node):
    stk = [node]

    while stk:
        node = stk.pop()
        print(node)

        if node.right: stk.append(node.right)
        if node.left: stk.append(node.left)

print()
print(pre_order_iterative(A)) # # 1 2 4 5 3 10

# Level Order Traversal (BFS)
# Time: O(n), Space O(n)
from collections import deque

def level_order(node):
    q = deque()
    q.append(node)

    while q:
        node = q.popleft()
        print(node)

        if node.left: q.append(node.left)
        if node.right: q.append(node.right)

print()
print(level_order(A)) # 1 2 3 4 5 10

# Check if value exists (DFS)
# Time: O(n), Space O(n)

def search(node, target):
    if not node:
        return False

    if node.value == target:
        return True

    return search(node.left, target) or search(node.right, target)

print()
print(search(A, 6)) # False
print(search(A, 10)) # True

# Binary Search Trees (BSTs)

#           5
#       1       8
#   -1     3 7      9

A1 = BSTNode(5)
B1 = BSTNode(1)
C1 = BSTNode(8)
D1 = BSTNode(-1)
E1 = BSTNode(3)
F1 = BSTNode(7)
G1 = BSTNode(9)

A1.left, A1.right = B1, C1
B1.left, B1.right = D1, E1
C1.left, C1.right = F1, G1

print()
print(A1) # 5

print(in_order(A1)) # -1 1 3 5 7 8 9

print(level_order(A1)) # 5 1 8 -1 3 7 9

def search_bst(node, target):
    if not node:
        return False

    if node.value == target:
        return True

    if target < node.value: return search_bst(node.left, target)
    else: return search_bst(node.right, target)

print()
print(search_bst(A1,-1)) # True
print(search_bst(C1,-1)) # False
