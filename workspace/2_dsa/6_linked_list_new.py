# Create own linked lists

# create a class to represent a linked list
class LinkedList:
    def __init__(self, nodes=None):
        self.head = None
        if nodes is not None:
            node = Node(data=nodes.pop(0))
            self.head = node
            for elem in nodes:
                node.next = Node(data=elem)
                node = node.next

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(node.data)
            node = node.next
        nodes.append("None")
        return " -> " . join(nodes)

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    # Inserting at the beginning
    def add_first(self, node):
        node.next = self.head
        self.head = node

    # Inserting at the End
    def add_last(self, node):
        if self.head is None:
            self.head = node
            return
        for current_node in self:
            pass
        current_node.next = node

    # Inserting Between Two Nodes
    # after
    def add_after(self, target_node, new_node):
        if self.head is None:
            raise Exception('List is empty')

        for node in self:
            if node.data == target_node:
                new_node.next = node.next
                node.next = new_node
                return

        raise Exception(f"Node with data {target_node} not found")
    # before
    def add_before(self, target_node, new_node):
        if self.head is None:
            raise Exception("List is empty")

        if self.head.data == target_node:
            return self.add_first(new_node)

        prev_node = self.head
        for node in self:
            if node.data == target_node:
                prev_node.next = new_node
                new_node.next = node
                return
            prev_node = node

        raise Exception(f"Node with data {target_node} not found")

    # Remove node
    def remove_node(self, target_node):
        if self.head is None:
            raise Exception('List is empty')

        if self.head.data == target_node:
            self.head = self.head.next
            return

        previous_node = self.head
        for node in self:
            if node.data == target_node:
                previous_node.next = node.next
                return
            previous_node = node

        raise Exception(f"Node with data {target_node} not found")

# create a class to represent each node of the linked list
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return self.data

llist = LinkedList()

node1 = Node('a')
llist.head = node1

print(llist) #a -> None

node2 = Node('b')
node3 = Node('c')

node1.next = node2
node2.next = node3

print(llist) # a -> b -> c -> None

print()

# traverse a linked list: Traversing means going through every single node,
# staring with the head of the linked list
# and ending on the node that has a next value of None.

traverse = LinkedList(["a", "b", "c", "d", "e"])

print(traverse) # a -> b -> c -> d -> e -> None

# Iterables
for node in traverse:
    print(node)

'''
a
b
c
d
e
'''

print()
# Inserting at the beginning
first_lists = LinkedList()

first_lists.add_first(Node('y'))
print(first_lists) # y -> None

first_lists.add_first(Node('z'))
print(first_lists) # z -> y -> None

print()
# Inserting at the End
last_lists = LinkedList(["a", "b", "c", "d"])

print(last_lists) # a -> b -> c -> d -> None

last_lists.add_last(Node('e'))
print(last_lists) # a -> b -> c -> d -> e -> None

last_lists.add_last(Node('f'))
print(last_lists) # a -> b -> c -> d -> e -> f -> None

print()
# Inserting Between Two Nodes
# after
# after_lists_exp = LinkedList()

# after_lists_exp.add_after('a', Node('b'))

# print(after_lists_exp) # excpetion raised

after_lists = LinkedList(["a", "b", "c", "d"])
print(after_lists) # a -> b -> c -> d -> None

after_lists.add_after('b', Node('bb'))
print(after_lists) # a -> b -> bb -> c -> d -> None

# after_lists.add_after('e', Node('f'))
# print(after_lists) # Exception: Node with data e not found

print()
# before
# before_lists = LinkedList()
# before_lists.add_before('a', Node('b'))

# print(before_lists) # raise Exception("List is empty")

before_lists = LinkedList(['y', 'z'])
print(before_lists) # y -> z -> None

before_lists.add_before('y', Node('x'))
print(before_lists) # x -> y -> z -> None

before_lists.add_before('y', Node('xx'))
print(before_lists) # x -> xx -> y -> z -> None

before_lists.add_before('z', Node('yy'))
print(before_lists) # x -> xx -> y -> yy -> z -> None

print()
# remove node
# remove_lists = LinkedList()
# remove_lists.remove_node('a')
# print(remove_lists) # Exception: List is empty

remove_lists = LinkedList(['a', 'b', 'c', 'd'])
print(remove_lists) # a -> b -> c -> d -> None

remove_lists.remove_node('d')
print(remove_lists) # a -> b -> c -> None

remove_lists.remove_node('d')
print(remove_lists) # Exception: Node with data d not found