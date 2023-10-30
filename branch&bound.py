import tkinter as tk
from collections import defaultdict, deque
import random

# This class represents a directed graph using an adjacency list representation
class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        self.graph[u].append(v)

# Initialize the Tkinter application
root = tk.Tk()
root.title("Branch and Bound Visualization")

# Create a canvas for drawing
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Create a Graph object and add edges
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

# Dictionary to store node coordinates
node_positions = {}

# Function to calculate and store node coordinates randomly on the canvas
def calculate_node_positions(graph, canvas_width, canvas_height):
    for node in graph.graph.keys():
        x = random.randint(20, canvas_width - 20)
        y = random.randint(20, canvas_height - 20)
        node_positions[node] = (x, y)

# Function to draw the graph
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

# Branch and Bound path
branch_and_bound_path = []

# Function to visualize Branch and Bound
def branch_and_bound(start_node, end_node):
    visited = set()
    stack = [(start_node, None)]
    while stack:
        current_node, parent = stack.pop()
        visited.add(current_node)
        if parent is not None:
            x1, y1 = node_positions[parent]
            x2, y2 = node_positions[current_node]
            canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="green")
            root.update()
        x, y = node_positions[current_node]
        if current_node == start_node:
            canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="blue")
        elif current_node == end_node:
            canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="red")
        else:
            canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="green")
        root.update()
        root.after(1000)
        branch_and_bound_path.append(current_node)
        if current_node == end_node:
            break
        next_nodes = g.graph[current_node]
        # Sort next nodes by some criterion, e.g., distance to the target
        next_nodes.sort(key=lambda node: abs(node - end_node))
        for neighbor in next_nodes:
            if neighbor not in visited:
                stack.append((neighbor, current_node))

    print("Branch and Bound Path:", branch_and_bound_path)

# Function to handle the Start Branch and Bound button
def start_branch_and_bound():
    start_node = int(start_entry.get())
    end_node = int(end_entry.get())
    branch_and_bound(start_node, end_node)

# Create buttons and entry fields for start and end nodes
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

start_button = tk.Button(root, text="Start Branch and Bound", command=start_branch_and_bound)
start_button.pack()

# Start the Tkinter main loop
root.mainloop()
