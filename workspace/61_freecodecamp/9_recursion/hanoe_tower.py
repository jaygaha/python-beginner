# Recursion: Recursion is a programming approach that allows you to solve complicated computational problems with just a little code.
# In this project, you'll start with a loop-based approach to solving the tower of Hanoi mathematical puzzle. Then you'll learn how to implement a recursive solution.

# def hanoe_tower(n):
#     if n == 1:
#         return 1
#     else:
#         return n * hanoe_tower(n - 1)

# print(hanoe_tower(4))

# create a function for recusion

my_graph = {
    # 'A': [('B', 3), ('D', 1)],
    # 'B': [('A', 3), ('C', 4)],
    # 'C': [('B', 4), ('D', 7)],
    # 'D': [('A', 1), ('C', 7)]

    # example2
    'A': [('B', 5), ('C', 3), ('E', 11)],
    'B': [('A', 5), ('C', 1), ('F', 2)],
    'C': [('A', 3), ('B', 1), ('D', 1), ('E', 5)],
    'D': [('C', 1), ('E', 9), ('F', 3)],
    'E': [('A', 11), ('C', 5), ('D', 9)],
    'F': [('B', 2), ('D', 3)]
}
def shortest_path(graph, start, target = ''):
    unvisited = list(graph)
    distances = {node: 0 if node == start else float('inf') for node in graph}
    paths = {node: [] for node in graph}
    paths[start].append(start)

    while unvisited:
        current = min(unvisited, key=distances.get)
        for node, distance in graph[current]:
            if distance + distances[current] < distances[node]:
                distances[node] = distance + distances[current]
                if paths[node] and paths[node][-1] == node:
                    paths[node] = paths[current][:]
                else:
                    paths[node].extend(paths[current])
                paths[node].append(node)
        unvisited.remove(current)

    targets_to_print = [target] if target else graph
    for node in targets_to_print:
        if node == start:
            continue
        print(f'\n{start}-{node} distance: {distances[node]}\nPath: {" -> ".join(paths[node])}')

    return distances, paths

# shortest_path(my_graph, 'A')

shortest_path(my_graph, 'A', 'F') # shortest path from A to F  ## A-F distance: 6 Path: A -> C -> B -> F
