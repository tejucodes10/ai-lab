import tkinter as tk
from collections import defaultdict, deque
import random

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        self.graph[u].append(v)

root = tk.Tk()
root.title("A* Visualization")

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

g = Graph()
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 3)
g.add_edge(3, 3)
g.add_edge(1, 4)
g.add_edge(4, 4)
g.add_edge(2, 5)
g.add_edge(2, 6)
g.add_edge(5, 5)
g.add_edge(6, 6)

node_positions = {}

def calculate_node_positions(graph, canvas_width, canvas_height):
    for node in graph.graph.keys():
        x = random.randint(20, canvas_width - 20)
        y = random.randint(20, canvas_height - 20)
        node_positions[node] = (x, y)

def draw_graph():
    canvas_width = canvas.winfo_reqwidth()
    canvas_height = canvas.winfo_reqheight()
    calculate_node_positions(g, canvas_width, canvas_height)

    for node, position in node_positions.items():
        x, y = position
        canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightblue")
        canvas.create_text(x, y, text=str(node))

    for u in g.graph:
        for v in g.graph[u]:
            x1, y1 = node_positions[u]
            x2, y2 = node_positions[v]
            canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)

    root.update()

a_star_path = []

class Node:
    def __init__(self, id, parent, cost, heuristic):
        self.id = id
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic

    def total_cost(self):
        return self.cost + self.heuristic

def a_star(start_node, end_node):
    open_list = [Node(start_node, None, 0, heuristic_estimate(start_node, end_node))]
    closed_list = set()

    while open_list:
        open_list.sort(key=lambda node: node.total_cost())
        current_node = open_list.pop(0)
        closed_list.add(current_node.id)

        if current_node.parent is not None:
            x1, y1 = node_positions[current_node.parent]
            x2, y2 = node_positions[current_node.id]
            canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="green")
            root.update()

        x, y = node_positions[current_node.id]
        if current_node.id == start_node:
            canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="blue")
        elif current_node.id == end_node:
            canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="red")
        else:
            canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="green")
        root.update()
        root.after(1000)
        a_star_path.append(current_node.id)
        if current_node.id == end_node:
            break

        for neighbor in g.graph[current_node.id]:
            if neighbor not in closed_list:
                cost = current_node.cost + 1
                heuristic = heuristic_estimate(neighbor, end_node)
                new_node = Node(neighbor, current_node.id, cost, heuristic)
                open_list.append(new_node)

    print("A* Path:", a_star_path)

def heuristic_estimate(node, end_node):
    # You can define your own heuristic function here (e.g., Euclidean distance)
    x1, y1 = node_positions[node]
    x2, y2 = node_positions[end_node]
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def start_a_star():
    start_node = int(start_entry.get())
    end_node = int(end_entry.get())
    a_star(start_node, end_node)

draw_button = tk.Button(root, text="Draw Graph", command=draw_graph)
draw_button.pack()

start_label = tk.Label(root, text="Start Node:")
start_label.pack()
start_entry = tk.Entry(root)
start_entry.pack()

end_label = tk.Label(root, text="End Node:")
end_label.pack()
end_entry = tk.Entry(root)
end_entry.pack()

start_button = tk.Button(root, text="Start A*", command=start_a_star)
start_button.pack()

root.mainloop()
