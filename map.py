import tkinter as tk
from tkinter import *
from tkinter import messagebox
import osmnx as ox
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.lines import Line2D
from algorithm import astar_path, bfs_path, dfs_path, dijkstra_path, bellman_ford

# Step 1: Load the graph
place_name = "Giang Vo, Ba Dinh, Hanoi, Vietnam"
graph_file = 'giang_vo_graph.graphml'

# Check if the graph file exists
graph = ox.load_graphml(graph_file)
# Initialize global variables
image_path = "giangvo.png"

# Step 2: Define GUI application
class MapApp:
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Path Finder Application")
        self.root.geometry("1200x800")
        self.selected_points = []
        self.start_node = None
        self.end_node = None
        self.routes = {}
        self.selected_algorithm = "A*"
        self.background_image = mpimg.imread(image_path)
        self.algorithm_color = {
            "A*": "blue",
            "BFS": "green",
            "DFS": "red",
            "Dijkstra": "purple",
            "Belllman_ford": "brown",
        }
        self.route_info = []

        # Main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)

        # Sidebar
        self.sidebar = tk.Frame(root, bg='#f0f0f0')
        self.sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.info_label = tk.Label(self.sidebar, text="Select 2 points", font=("Arial", 12))
        self.info_label.pack(pady=10)

        self.algorithm_label = tk.Label(self.sidebar, text="Algorithm", font=("Arial", 12))
        self.algorithm_label.pack(pady=5)

        self.algorithm_var = tk.StringVar(self.sidebar)
        self.algorithm_var.set(self.selected_algorithm)
        self.algorithm_dropdown = tk.OptionMenu(self.sidebar, self.algorithm_var, "A*", "BFS", "DFS", "Dijkstra", "Greedy", "SPFA", command=self.change_algorithm)
        self.algorithm_dropdown.pack(pady=5, fill=tk.X)

        # Buttons
        self.find_button = tk.Button(self.sidebar, text="Find Path", command=self.calculate_route, font=("Arial", 12))
        self.find_button.pack(fill=tk.X, pady=5)

        self.reset_button = tk.Button(self.sidebar, text="Reset", command=self.reset_selection, font=("Arial", 12))
        self.reset_button.pack(fill=tk.X, pady=5)

        self.quit_button = tk.Button(self.sidebar, text="Exit", command=self.root.quit, bg="red", fg="white", font=("Arial", 12))
        self.quit_button.pack(fill=tk.X, pady=5)

        # Route Information
        self.info_frame = tk.Frame(self.main_frame)
        self.info_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        self.route_info_label = tk.Label(self.info_frame, text="Route Info", font=("Arial", 12, "bold"))
        self.route_info_label.pack(pady=5)

        self.route_info_text = tk.Text(self.info_frame, height=5, font=("Arial", 12))
        self.route_info_text.pack(fill=tk.X, padx=5)
        self.route_info_text.config(state=tk.DISABLED)

        # Canvas for Graph
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(in_=self.main_frame, side=tk.TOP, fill=tk.BOTH, expand=True)
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)

        # Plot Graph
        self.plot_graph()
        self.root.mainloop()

    def change_algorithm(self, algorithm):
        self.selected_algorithm = algorithm
        messagebox.showinfo("Algorithm Changed", f"Using {algorithm}")

    def plot_graph(self):
        self.ax.clear()
        # Vẽ nền trước khi vẽ các đối tượng khác
        self.ax.imshow(self.background_image, extent=[21.0234381, 21.0311603, 105.8112969, 105.8247374], aspect='auto', zorder=0)

        # Vẽ đồ thị sau khi nền đã được vẽ
        ox.plot_graph(graph, ax=self.ax, show=False, close=False, bgcolor="white", edge_color='none', node_size=0)

        # Thêm chú thích cho các thuật toán
        handles = [Line2D([0], [0], color=color, lw=2, label=algorithm) for algorithm, color in self.algorithm_color.items()]
        self.ax.legend(handles=handles, loc="upper right")
        self.canvas.draw()

    def on_click(self, event):
        if event.xdata and event.ydata:
            nearest_node = ox.distance.nearest_nodes(graph, X=event.xdata, Y=event.ydata)
            self.selected_points.append(nearest_node)
            self.ax.scatter(event.xdata, event.ydata, c="blue", s=50, zorder=5)
            self.canvas.draw()

    def calculate_route(self):
        if len(self.selected_points) < 2:
            messagebox.showwarning("Error", "Select 2 points first!")
            return

        self.start_node = self.selected_points[0]
        self.end_node = self.selected_points[1]

        if self.selected_algorithm == "A*":
            path = astar_path(graph, self.start_node, self.end_node)
        elif self.selected_algorithm == "BFS":
            path = bfs_path(graph, self.start_node, self.end_node)
        elif self.selected_algorithm == "DFS":
            path = dfs_path(graph, self.start_node, self.end_node)
        elif self.selected_algorithm == "Dijkstra":
            path = dijkstra_path(graph, self.start_node, self.end_node)
        elif self.selected_algorithm == "Greedy":
            path = bellman_ford(graph, self.start_node, self.end_node)

        if path:
            route_length = nx.path_weight(graph, path, weight='length')
            self.route_info_text.config(state=tk.NORMAL)
            self.route_info_text.delete('1.0', tk.END)
            self.route_info_text.insert(tk.END, f"Length: {route_length:.2f} meters\nPath: {path}")
            self.route_info_text.config(state=tk.DISABLED)

            self.ax.plot(*zip(*[(graph.nodes[node]['x'], graph.nodes[node]['y']) for node in path]), color=self.algorithm_color[self.selected_algorithm], linewidth=2, zorder=4)
            self.canvas.draw()

    def reset_selection(self):
        self.selected_points.clear()
        self.routes.clear()
        self.plot_graph()

if __name__ == "__main__":
    root = tk.Tk()
    app = MapApp(root)
