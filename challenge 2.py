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
        if start == end and len(path) > 1:
            return [path]
        if start not in self.graph:
            return []
        
        paths = []
        for node in self.graph[start]:
            if node not in path or node == end:
                new_paths = self.find_all_paths(node, end, path)
                for new_path in new_paths:
                    paths.append(new_path)
        
        return paths
    
    def find_cycles(self, start, current, visited, path, cycles):
        path.append(current)
        visited.add(current)
        
        for neighbor in self.graph[current]:
            if neighbor == start and len(path) > 2:
                cycles.append(path + [start])
            elif neighbor not in visited:
                self.find_cycles(start, neighbor, visited.copy(), path[:], cycles)
    
    def get_cycles(self, start):
        cycles = []
        self.find_cycles(start, start, set(), [], cycles)
        return cycles
    
    def shortest_longest_cycle(self, start):
        cycles = self.get_cycles(start)
        if not cycles:
            return None, None
        
        cycles.sort(key=len)
        return cycles[0], cycles[-1]

# Definisi graf berdasarkan gambar
g = Graph()
edge_list = [
    ('A', 'B'), ('A', 'D'), ('B', 'C'), ('B', 'E'), ('C', 'F'),
    ('D', 'E'), ('E', 'F'), ('B', 'D'), ('C', 'E')
]

for u, v in edge_list:
    g.add_edge(u, v)

print("Semua kemungkinan path dari A ke C:")
for path in g.find_all_paths('A', 'C'):
    print(path)
print()

print("Semua cycle jika C adalah titik awal:")
for cycle in g.get_cycles('C'):
    print(cycle)
print()

print("Semua cycle jika B adalah titik awal:")
for cycle in g.get_cycles('B'):
    print(cycle)
print()

shortest, longest = g.shortest_longest_cycle('A')
print("Circuit terpendek dari A ke A:")
print(shortest)
print()
print("Circuit terpanjang dari A ke A:")
print(longest)
