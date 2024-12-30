import tkinter as tk
from tkinter import *
from tkinter import messagebox
import osmnx as ox
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.lines import Line2D
from algorithm import a_star, bfs, dfs, dijkstra, nearest_node, heuristic, bellman_ford
place_name = "Giang Vo, Ba Dinh, Hanoi, Vietnam"
graph_file = 'giang_vo_graph.graphml'

# Check if the graph file exists
graph = ox.load_graphml(graph_file)
# Initialize global variables
image_path = "image.png"

# Step 2: Define GUI application
class MapApp:
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Shortest Path Finder")
        self.root.state("zoomed") 
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
            "Bellman-Ford": "brown",
        }
        self.route_info = []
        # Main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        # Sidebar for buttons
        self.sidebar = tk.Frame(root)
        self.sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        # Create a label to show node selection
        self.info_label = tk.Label(self.sidebar, text="Select two points on the map", font=("Arial", 14))
        self.info_label.pack(pady=10)
        # Drop bar menu for selecting algorithms
        self.algorithm_label = tk.Label(self.sidebar, text="Select Algorithm", font=("Arial", 14))
        self.algorithm_label.pack(pady = 5)
        
        self.algorithm_var = tk.StringVar(self.sidebar)
        self.algorithm_var.set(self.selected_algorithm)
        self.sidebar.option_add("*TMenubutton*Font", ("Arial", 14))
        self.algorithm_dropdown = tk.OptionMenu(self.sidebar, self.algorithm_var, "A*", "BFS", "DFS", "Dijkstra", "Greedy", "SPFA", command = self.change_algorithm)
        self.algorithm_dropdown.pack(pady = 5, fill=tk.X)
        # Create buttons
        self.quit_button = tk.Button(self.sidebar, text="Exit", command=self.root.quit, bg = "red", fg = "white", font = ("Arial", 14))
        self.quit_button.pack(side=tk.BOTTOM, pady = 5, fill=tk.X)
        self.reset_button = tk.Button(self.sidebar, text="Reset", command=self.reset_selection, font= ("Arial", 14))
        self.reset_button.pack(fill=tk.X, pady = 5, side = tk.BOTTOM)
        self.find_button = tk.Button(self.sidebar, text="Find Path", command=self.calculate_route, font= ("Arial", 14))
        self.find_button.pack(fill=tk.X, pady=5)
        self.show_all_node = tk.Button(self.sidebar, text="Show All Nodes, Path", command=self.show_all_nodes, font= ("Arial", 14))
        self.show_all_node.pack(fill= tk.X, pady=5)
        # Embed the canvas in the GUI
        
        self.info_frame = tk.Frame(self.main_frame)
        self.info_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        self.route_info_label = tk.Label(self.info_frame, text="Route Information", font=("Arial", 12, "bold"))
        self.route_info_label.pack(pady=5)

        self.route_info_text = tk.Text(self.info_frame, height=5, font=("Arial", 12))
        self.route_info_text.pack(fill=tk.X, padx=5)
        self.route_info_text.config(state=tk.DISABLED)
        # Connect matplotlib events to Tkinter
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(in_= self.main_frame,side=tk.TOP, fill=tk.BOTH, expand=True)
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        self.plot_graph()
        self.root.mainloop()
    def show_all_nodes(self):
        """Show all nodes and edges in the graph."""
        self.ax.clear()
        self.ax.imshow(self.background_image, extent=[105.8112969, 105.8247374, 21.0234381, 21.0311603], aspect='auto', zorder=0)
        ox.plot_graph(graph, ax=self.ax, show=False, close=False, bgcolor="lightgray", edge_color='blue', node_size=30, node_color='red', edge_linewidth=2)
        self.canvas.draw()
    def change_algorithm(self, algorithm):
        """Change the selected algorithm."""
        previous_algorithm = self.selected_algorithm
        self.selected_algorithm = algorithm
        messagebox.showinfo("Algorithm Changed", f"Algorithm changed from {previous_algorithm} to {algorithm}")
    def plot_graph(self):
        """Plot the graph in the matplotlib figure."""
        self.ax.clear()
        self.ax.imshow(self.background_image, extent=[105.8112969, 105.8247374, 21.0234381, 21.0311603], aspect='auto', zorder=0)
        ox.plot_graph(graph, ax=self.ax, show=False, close=False, bgcolor="lightgray", edge_color='none', node_size=0)
        for algorithm, route in self.routes.items():
            ox.plot_graph_route(
                graph,
                route,
                route_color=self.algorithm_color[algorithm],
                route_linewidth=3,
                bgcolor="lightgray",
                ax=self.ax,
                show=False,
                close=False,
            )
        # Add legend
        handles = [Line2D([0], [0], color=color, lw=2, label=algorithm)
                   for algorithm, color in self.algorithm_color.items()]
        self.ax.legend(handles=handles, loc="upper right")

        # Plot start and end points
        x_start, y_start = self.selected_points[0] if len(self.selected_points) > 0 else (None, None)
        x_end, y_end = self.selected_points[1] if len(self.selected_points) > 1 else (None, None)
        if self.start_node:
            self.ax.plot([x_start, graph.nodes[self.start_node]['x']], [y_start, graph.nodes[self.start_node]['y']], c="purple", linestyle="--", linewidth=3)
        if self.end_node:
            self.ax.plot([x_end, graph.nodes[self.end_node]['x']], [y_end, graph.nodes[self.end_node]['y']], c="purple", linestyle="--", linewidth=3)
        if x_start and y_start:
            self.ax.scatter(x_start, y_start, c="green", s=50, zorder=5)
        if x_end and y_end:
            self.ax.scatter(x_end, y_end, c="blue", s=50, zorder=5)
        self.canvas.draw()

    def on_click(self, event):
        """Handle click events to capture coordinates."""
        if event.xdata is None or event.ydata is None:
            return  # Ignore clicks outside the grap

        # Add the selected node to the points
        self.selected_points.append((event.xdata, event.ydata))
        print(f"Selected points: {event.xdata}, {event.ydata}")

        # Plot the selected node immediately
        self.ax.scatter(event.xdata, event.ydata, c="blue", s=50, zorder=5)
        self.canvas.draw()

    def calculate_route(self):
        """Calculate and display the shortest route."""
        if len(self.selected_points) != 2:
            messagebox.showwarning("Selection Error", "Please select two points before calculating.")
            return
        if self.selected_algorithm == "DFS" or self.selected_algorithm == "BFS":
            start,_ = nearest_node(graph, [self.selected_points[0][0], self.selected_points[0][1]], k=1, heuristic= heuristic)
            end,_ = nearest_node(graph, [self.selected_points[1][0], self.selected_points[1][1]], k=1, heuristic= heuristic)
            self.start_node = start[0]
            self.end_node = end[0]
            if self.selected_algorithm == "DFS":
                path = dfs(graph, self.start_node, self.end_node)
            else:
                path, _ = bfs(graph, self.start_node, self.end_node)
            if path is None:
                messagebox.showwarning("No Path", "No path found between the selected points.")
                return
            self.routes[self.selected_algorithm] = path
            min_dis = sum(graph[path[i]][path[i + 1]][0].get('length') for i in range(len(path) - 1))
            self.route_info.append(f"Algorithm: {self.selected_algorithm}, Distance: {min_dis} meters")
            self.route_info_text.config(state=tk.NORMAL)
            self.route_info_text.delete(1.0, tk.END)
            self.route_info_text.insert(tk.END, "\n".join(self.route_info))
            self.route_info_text.config(state=tk.DISABLED)
            self.plot_graph()
            return
        else:
            near_start, distance_start = nearest_node(graph, [self.selected_points[0][0], self.selected_points[0][1]], k= 3, heuristic= heuristic)
            near_end, distance_end = nearest_node(graph, [self.selected_points[1][0], self.selected_points[1][1]], k= 3, heuristic= heuristic)
            min_i, min_j = None, None
            dis_min = float('inf')
            min_path = None
            check = False
            if self.selected_algorithm == "A*":
                for id1, i in enumerate(near_start):
                    for id2, j in enumerate(near_end):
                        path, dis = a_star(graph, i, j, heuristic= heuristic)
                        if path is None:
                            continue
                        dis += (distance_start[id1] + distance_end[id2])
                        if dis < dis_min:
                            dis_min = dis
                            min_i, min_j = i, j
                            min_path = path
                            check = True
                if not check:
                    messagebox.showwarning("No Path", "No path found between the selected points.")
                    return
            elif self.selected_algorithm == "Dijkstra":
                for id1, i in enumerate(near_start):
                    for id2, j in enumerate(near_end):
                        path, dis = dijkstra(graph, i, j)
                        if path is None:
                            continue
                        dis += (distance_start[id1] + distance_end[id2])
                        if dis < dis_min:
                            dis_min = dis
                            min_i, min_j = i, j
                            min_path = path
                            check = True
                if not check:
                    messagebox.showwarning("No Path", "No path found between the selected points.")
                    return
            elif self.selected_algorithm == "Bellman-Ford":
                for id1, i in enumerate(near_start):
                    for id2, j in enumerate(near_end):
                        path, dis = bellman_ford(graph, i, j)
                        if path is None:
                            continue
                        dis += (distance_start[id1] + distance_end[id2])
                        if dis < dis_min:
                            dis_min = dis
                            min_i, min_j = i, j
                            min_path = path
                            check = True
                if not check:
                    messagebox.showwarning("No Path", "No path found between the selected points.")
                    return
            self.start_node = min_i
            self.end_node = min_j
            self.routes[self.selected_algorithm] = min_path
            self.route_info.append(f"Algorithm: {self.selected_algorithm}, Distance: {dis_min} meters")
            self.route_info_text.config(state=tk.NORMAL)
            self.route_info_text.delete(1.0, tk.END)
            self.route_info_text.insert(tk.END, "\n".join(self.route_info))
            self.route_info_text.config(state=tk.DISABLED)
            self.plot_graph()
    def reset_selection(self):
        """Reset the map and clear selections."""
        self.selected_points = []
        self.start_node = None
        self.end_node = None
        self.routes = {}
        self.route_info = []
        self.info_label.config(text="Select two points on the map")
        self.route_info_text.config(state=tk.NORMAL)
        self.route_info_text.delete(1.0, tk.END)
        self.route_info_text.config(state=tk.DISABLED)
        self.plot_graph()  # Redraw the map without the route


# Step 3: Run the application
root = tk.Tk()
app = MapApp(root)

