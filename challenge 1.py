from colorama import Fore, Style

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
    
    def find_trails(self, start, end, visited, path, trails):
        path.append(start)
        if start == end:
            trails.append(path[:])
        else:
            for neighbor in self.graph[start]:
                if (start, neighbor) not in visited and (neighbor, start) not in visited:
                    visited.add((start, neighbor))
                    self.find_trails(neighbor, end, visited, path, trails)
                    visited.remove((start, neighbor))
        path.pop()
    
    def find_paths(self, start, end, visited, path, paths):
        path.append(start)
        if start == end:
            paths.append(path[:])
        else:
            visited.add(start)
            for neighbor in self.graph[start]:
                if neighbor not in visited:
                    self.find_paths(neighbor, end, visited, path, paths)
            visited.remove(start)
        path.pop()
    
    def find_cycles(self, start, current, visited, path, cycles):
        path.append(current)
        visited.add(current)
        for neighbor in self.graph[current]:
            if neighbor == start and len(path) > 2:
                cycles.append(path[:])
            elif neighbor not in visited:
                self.find_cycles(start, neighbor, visited, path, cycles)
        path.pop()
        visited.remove(current)

g = Graph()
edges = [('A', 'B'), ('A', 'C'), ('B', 'C'), ('B', 'D'), ('C', 'D')]
for u, v in edges:
    g.add_edge(u, v)

trails = []
g.find_trails('A', 'D', set(), [], trails)
print("Trail dari A ke D:")
for trail in trails:
    print(Fore.CYAN + str(trail) + Style.RESET_ALL)

paths = []
g.find_paths('A', 'D', set(), [], paths)
print("\nSemua Path dari A ke D:")
for path in paths:
    print(Fore.GREEN + str(path) + Style.RESET_ALL)

cycles = []
g.find_cycles('A', 'A', set(), [], cycles)
print("\nSemua Cycle dari A:")
for cycle in cycles:
    print(Fore.RED + str(list(cycle)) + Style.RESET_ALL)