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
root.title("BFS Visualization")

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

# BFS traversal path
bfs_path = []

# Function to visualize BFS traversal
def bfs_traversal(start_node, end_node):
    visited = set()
    queue = deque([(start_node, None)])  # Add None for the starting node to indicate the start
    while queue:
        current_node, parent = queue.popleft()
        if parent is not None:
            x1, y1 = node_positions[parent]
            x2, y2 = node_positions[current_node]
            canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="green")
            root.update()
        x, y = node_positions[current_node]
        if current_node == start_node:
            canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="blue")  # Start node in blue
        elif current_node == end_node:
            canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="red")  # End node in red
        else:
            canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="green")  # Other nodes in green
        root.update()
        root.after(1000)  # Delay for visualization (1 second)
        bfs_path.append(current_node)  # Add the current node to the path

        if current_node == end_node:
            break

        visited.add(current_node)

        for neighbor in g.graph[current_node]:
            if neighbor not in visited and neighbor not in (node for node, _ in queue):
                queue.append((neighbor, current_node))

    print("BFS Traversal Path:", bfs_path)

# Function to handle the Start BFS button
def start_bfs():
    start_node = int(start_entry.get())
    end_node = int(end_entry.get())
    bfs_traversal(start_node, end_node)

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

start_button = tk.Button(root, text="Start BFS Traversal", command=start_bfs)
start_button.pack()

# Start the Tkinter main loop
root.mainloop()
