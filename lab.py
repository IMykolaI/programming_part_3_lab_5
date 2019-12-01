import unittest
import time


class Vertex:
    def __init__(self, label):
        self.label = label
        self.outbound_edges = []


class Edge:
    def __init__(self, start_vertex, end_vertex):
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex


class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges


def bfs(graph, start_vertex):
    lengths = {start_vertex.label: 0}
    queue = [start_vertex]
    visited = {vertex.label: False for vertex in graph.vertices}
    while len(queue) > 0:
        current_vertex = queue.pop(0)
        if visited[current_vertex.label]:
            continue
        visited[current_vertex.label] = True
        for edge in current_vertex.outbound_edges:
            if current_vertex.label not in lengths.keys():
                if edge.end_vertex.label not in lengths.keys():
                    lengths[edge.end_vertex.label] = 1
                elif lengths[edge.end_vertex.label] > 1:
                    lengths[edge.end_vertex.label] = 1
            else:
                if edge.end_vertex.label in lengths.keys():
                    if lengths[edge.end_vertex.label] > lengths[current_vertex.label] + 1:
                        lengths[edge.end_vertex.label] = lengths[current_vertex.label] + 1
                else:
                    lengths[edge.end_vertex.label] = lengths[current_vertex.label] + 1
        neighbors = [
            edge.end_vertex
            for edge in current_vertex.outbound_edges
            if not visited[edge.end_vertex.label]
        ]
        queue.extend(neighbors)
    return lengths


def check_word_in(find_word_in, word_in):
    for char in find_word_in:
        if char in word_in:
            next_start = word_in.index(char)
            word_in = word_in[next_start + 1:]
        else:
            return False
    return True


def get_data(file_in):
    result_array = []
    for line in file_in:
        result_array.append(line.split('\n')[0])
    if len(result_array) - 1 != int(result_array[0]):
        raise Exception(f'Wrong number of words (Given: {len(result_array) - 1}; Expected: {result_array[0]})')
    return sorted(result_array[1:], key=len)


def create_graph(data_in):
    vertices = []
    edges = []

    for node in data_in:
        vertices.append(Vertex(node))

    for i in range(len(vertices) - 1):
        for j in range(1, len(vertices)):
            if len(vertices[j].label) - len(vertices[i].label) == 1:
                if check_word_in(vertices[i].label, vertices[j].label):
                    edges.append([vertices[j], vertices[i]])
            elif len(vertices[j].label) - len(vertices[i].label) > 1:
                break

    for vertex in vertices:
        for found_edge in edges:
            if vertex.label == found_edge[0].label:
                vertex.outbound_edges.append(Edge(found_edge[0], found_edge[1]))

    graph = Graph(vertices, edges)
    return graph


def get_longest_chain(graph_in, start_node):
    chain = dict()
    result = bfs(graph_in, start_node)
    result = dict([(value, key) for key, value in result.items()])
    road = [value for key, value in result.items()]
    road.sort(key=len, reverse=True)
    chain['length'] = len(road)
    chain['road'] = road
    return chain


# Program

file = None

try:
    choose_file = int(input('\nChoose file with words:\n1 - test1\n2 - test2\n3 - test3\nAnswer : '))
except ValueError:
    raise Exception('\nYou have entered wrong type.')

if choose_file == 1:
    file = open('test1.txt', 'r')
elif choose_file == 2:
    file = open('test2.txt', 'r')
elif choose_file == 3:
    file = open('test3.txt', 'r')
else:
    raise Exception(f'\nNumber out of range: You entered {choose_file}.')

array_in = get_data(file)

file.close()

got_graph = create_graph(array_in)

got_vertices = got_graph.vertices

print('\nAvailable words:')
for vertex in got_vertices:
    print(f'{got_vertices.index(vertex) + 1} - {vertex.label}')
answer = input('\nChoose any word to start : ')

got_chain = get_longest_chain(got_graph, got_vertices[int(answer) - 1])

chain_length = got_chain['length']
got_road = got_chain['road']
answer_string = ''
for i in range(chain_length):
    if i != chain_length - 1:
        answer_string += got_road[i] + ' => '
    else:
        answer_string += got_road[i]

print(f'\nMax road length: {chain_length} ({answer_string})')

print('\n\nUnittest results will be ready in 1 second. Please, stay here...')
time.sleep(1)


class UnitTest(unittest.TestCase):

    def test_find_longest_road_file_1(self):
        test_file = open('test1.txt', 'r')
        test_data = get_data(test_file)
        test_file.close()
        test_graph = create_graph(test_data)
        test_labels = {test_vertex: len(test_vertex.label) for test_vertex in test_graph.vertices}
        test_chain = get_longest_chain(test_graph, max(test_labels, key=test_labels.get))
        self.assertEqual(test_chain['length'], 6)

    def test_find_longest_road_file_2(self):
        test_file = open('test2.txt', 'r')
        test_data = get_data(test_file)
        test_file.close()
        test_graph = create_graph(test_data)
        test_labels = {test_vertex: len(test_vertex.label) for test_vertex in test_graph.vertices}
        test_chain = get_longest_chain(test_graph, max(test_labels, key=test_labels.get))
        self.assertEqual(test_chain['length'], 4)

    def test_find_longest_road_file_3(self):
        test_file = open('test3.txt', 'r')
        test_data = get_data(test_file)
        test_file.close()
        test_graph = create_graph(test_data)
        test_labels = {test_vertex: len(test_vertex.label) for test_vertex in test_graph.vertices}
        test_chain = get_longest_chain(test_graph, max(test_labels, key=test_labels.get))
        self.assertEqual(test_chain['length'], 1)


if __name__ == '__main__':
    unittest.main()
