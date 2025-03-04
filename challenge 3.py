class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append(v)
        self.graph[v].append(u)

    def find_all_paths(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in self.graph:
            return []
        paths = []
        for node in self.graph[start]:
            if node not in path:
                new_paths = self.find_all_paths(node, end, path)
                for new_path in new_paths:
                    paths.append(new_path)
        return paths

    def find_cycles(self, start, visited=None, path=[]):
        if visited is None:
            visited = set()
        visited.add(start)
        path.append(start)
        cycles = []
        for neighbor in self.graph[start]:
            if neighbor in path and len(path) > 2 and neighbor == path[0]:
                cycles.append(path[:])
            elif neighbor not in visited:
                cycles.extend(self.find_cycles(neighbor, visited.copy(), path[:]))
        return cycles

    def find_circuits(self, start):
        cycles = self.find_cycles(start)
        if not cycles:
            return None, None
        shortest = min(cycles, key=len)
        longest = max(cycles, key=len)
        return shortest, longest


g = Graph()
edges = [('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'E'), ('B', 'F'), ('C', 'F'), ('C', 'D'), ('D', 'F'), 
         ('E', 'H'), ('E', 'K'), ('F', 'I'), ('F', 'J'), ('G', 'H'), ('G', 'I'), ('H', 'K'), ('I', 'J'), ('K', 'J')]

for u, v in edges:
    g.add_edge(u, v)

print("1. Semua kemungkinan path dari A ke K:")
print(g.find_all_paths('A', 'K'))

print("2. Semua kemungkinan path dari G ke J:")
print(g.find_all_paths('G', 'J'))

print("3. Semua kemungkinan path dari E ke F:")
print(g.find_all_paths('E', 'F'))

print("4. Semua kemungkinan cycle jika A adalah titik awal:")
print(g.find_cycles('A'))

print("5. Semua kemungkinan cycle jika K adalah titik awal:")
print(g.find_cycles('K'))

print("6. Circuit terpendek dan terpanjang dari A ke A:")
print(g.find_circuits('A'))

print("7. Circuit terpendek dan terpanjang dari G ke G:")
print(g.find_circuits('G'))

print("8. Circuit terpendek dan terpanjang dari E ke E:")
print(g.find_circuits('E'))
