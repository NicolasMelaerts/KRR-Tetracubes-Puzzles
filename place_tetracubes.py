import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from matplotlib.widgets import Button
from draw_tetracubes import get_all_rotations

def draw_cube(ax, position, color='blue', alpha=0.7):
    """Draw a single cube at the specified position."""
    x, y, z = position
    vertices = [
        [(x, y, z), (x+1, y, z), (x+1, y+1, z), (x, y+1, z)],
        [(x, y, z+1), (x+1, y, z+1), (x+1, y+1, z+1), (x, y+1, z+1)],
        [(x, y, z), (x, y, z+1), (x, y+1, z+1), (x, y+1, z)],
        [(x+1, y, z), (x+1, y, z+1), (x+1, y+1, z+1), (x+1, y+1, z)],
        [(x, y, z), (x+1, y, z), (x+1, y, z+1), (x, y, z+1)],
        [(x, y+1, z), (x+1, y+1, z), (x+1, y+1, z+1), (x, y+1, z+1)]
    ]
    
    cube = Poly3DCollection(vertices, alpha=alpha)
    cube.set_facecolor(color)
    cube.set_edgecolor('black')
    ax.add_collection3d(cube)
    return cube

# Définitions des tétracubes de base
tetracube_I = [(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 0, 3)]
tetracube_T = [(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 1)]
tetracube_L = [(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 0)]
tetracube_Pyramid = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0)]
tetracube_O = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1)]
tetracube_N = [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 2)]
tetracube_Z = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 1, 0)]
tetracube_Z_mirror = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 1)]

# Générer toutes les rotations pour chaque tétracube
tetracube_I_rotated = get_all_rotations(tetracube_I)
tetracube_T_rotated = get_all_rotations(tetracube_T)
tetracube_L_rotated = get_all_rotations(tetracube_L)
tetracube_Pyramid_rotated = get_all_rotations(tetracube_Pyramid)
tetracube_O_rotated = get_all_rotations(tetracube_O)
tetracube_N_rotated = get_all_rotations(tetracube_N)
tetracube_Z_rotated = get_all_rotations(tetracube_Z)
tetracube_Z_mirror_rotated = get_all_rotations(tetracube_Z_mirror)

# Dictionnaire de toutes les rotations
all_rotations = {
    "I": tetracube_I_rotated,
    "T": tetracube_T_rotated,
    "L": tetracube_L_rotated,
    "Pyramid": tetracube_Pyramid_rotated,
    "O": tetracube_O_rotated,
    "N": tetracube_N_rotated,
    "Z": tetracube_Z_rotated,
    "Z_mirror": tetracube_Z_mirror_rotated
}

class SolutionVisualizer:
    def __init__(self, solution, cube_type="2x4x4"):
        self.solution = solution
        self.cube_type = cube_type
        
        # Set dimensions based on cube type
        if cube_type == "2x2x8":
            self.width = 8
            self.height = 2
            self.depth = 2
        else:  # Default to 2x4x4
            self.width = 4
            self.height = 4
            self.depth = 2
        
        # Parse the solution
        self.assign_type = {}
        self.positions = {}
        
        for item in solution.split():
            if item.startswith("assignType"):
                parts = item.replace("assignType(", "").replace(")", "").split(",")
                id_num = int(parts[0])
                type_name = parts[1].strip('"')
                self.assign_type[id_num] = type_name
            elif item.startswith("position"):
                parts = item.replace("position(", "").replace(")", "").split(",")
                id_num = int(parts[0])
                rotation = int(parts[1])
                x, y, z = int(parts[2]), int(parts[3]), int(parts[4])
                self.positions[id_num] = (rotation, x, y, z)
        
        # Define colors for each tetracube type
        self.colors = {
            "I": "red",
            "T": "blue",
            "L": "green",
            "Pyramid": "purple",
            "O": "orange",
            "N": "yellow",
            "Z": "cyan",
            "Z_mirror": "magenta"
        }
        
        # Setup the figure
        self.fig = plt.figure(figsize=(12, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Current number of tetracubes to display (0 to start)
        self.num_tetracubes = 0
        self.max_tetracubes = len(self.assign_type)
        
        # Get sorted tetracube IDs
        self.tetracube_ids = sorted(self.assign_type.keys())
        
        # Store tetracube collections
        self.tetracube_collections = {}
        
        # Create buttons
        self.ax_prev = plt.axes([0.7, 0.05, 0.1, 0.075])
        self.ax_next = plt.axes([0.81, 0.05, 0.1, 0.075])
        self.btn_prev = Button(self.ax_prev, 'Previous')
        self.btn_next = Button(self.ax_next, 'Next')
        self.btn_prev.on_clicked(self.prev_tetracube)
        self.btn_next.on_clicked(self.next_tetracube)
        
        # Initialize the plot
        self.update_plot()
    
    def prev_tetracube(self, event):
        self.num_tetracubes = max(0, self.num_tetracubes - 1)
        self.update_plot()
    
    def next_tetracube(self, event):
        self.num_tetracubes = min(self.max_tetracubes, self.num_tetracubes + 1)
        self.update_plot()
    
    def update_plot(self):
        # Clear the plot
        self.ax.clear()
        
        # Set labels and limits
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_xlim([0, self.width])
        self.ax.set_ylim([0, self.height])
        self.ax.set_zlim([0, self.depth])
        
        # Draw grid lines
        for i in range(self.width + 1):
            for j in range(self.height + 1):
                self.ax.plot([i, i], [j, j], [0, self.depth], 'k-', alpha=0.1)
                
        for i in range(self.width + 1):
            for k in range(self.depth + 1):
                self.ax.plot([i, i], [0, self.height], [k, k], 'k-', alpha=0.1)
                
        for j in range(self.height + 1):
            for k in range(self.depth + 1):
                self.ax.plot([0, self.width], [j, j], [k, k], 'k-', alpha=0.1)
        
        # Draw tetracubes
        if self.num_tetracubes == 0:
            title = f"Empty {self.cube_type} Grid"
        else:
            # Draw the first n tetracubes
            for i in range(self.num_tetracubes):
                if i < len(self.tetracube_ids):
                    id_num = self.tetracube_ids[i]
                    self.draw_tetracube(id_num)
            
            if self.num_tetracubes == self.max_tetracubes:
                title = f"All Tetracubes in {self.cube_type}"
            else:
                title = f"First {self.num_tetracubes} Tetracubes in {self.cube_type}"
        
        # Add a legend
        from matplotlib.lines import Line2D
        legend_elements = [Line2D([0], [0], marker='s', color='w', 
                                 markerfacecolor=self.colors[type_name], markersize=10, label=type_name)
                          for type_name in self.colors]
        self.ax.legend(handles=legend_elements, loc='upper right')
        
        # Add counter
        plt.title(f"{title} ({self.num_tetracubes}/{self.max_tetracubes})")
        plt.tight_layout()
        self.fig.canvas.draw_idle()
    
    def draw_tetracube(self, id_num):
        type_name = self.assign_type[id_num]
        rotation_id, x, y, z = self.positions[id_num]
        color = self.colors[type_name]
        
        # Get the tetracube shape based on rotation
        if type_name in all_rotations and 0 <= rotation_id-1 < len(all_rotations[type_name]):
            shape = all_rotations[type_name][rotation_id-1]
            
            # Draw each cube in the tetracube
            cubes = []
            for dx, dy, dz in shape:
                cube = draw_cube(self.ax, (x + dx, y + dy, z + dz), color)
                cubes.append(cube)
            
            self.tetracube_collections[id_num] = cubes
        else:
            print(f"Warning: Tetracube {type_name} with rotation {rotation_id} not found")
    
    def show(self):
        plt.show()

def visualize_solution(solution, cube_type="2x4x4"):
    """Visualize the solution with interactive navigation."""
    visualizer = SolutionVisualizer(solution, cube_type)
    visualizer.show()

# Example usage with the solutions
solution_2x4x4 = "assignType(1,\"O\") assignType(2,\"Z\") assignType(3,\"L\") assignType(4,\"Z_mirror\") assignType(5,\"T\") assignType(6,\"Pyramid\") assignType(7,\"N\") assignType(8,\"I\") position(1,1,3,0,0) position(8,2,0,0,0) position(6,5,2,2,0) position(2,6,1,0,0) position(4,6,0,1,0) position(7,11,0,0,0) position(5,12,1,2,0) position(3,20,0,2,1)"

solution_2x2x8 = "assignType(1,\"I\") assignType(2,\"T\") assignType(3,\"L\") assignType(4,\"Pyramid\") assignType(5,\"O\") assignType(6,\"N\") assignType(7,\"Z\") assignType(8,\"Z_mirror\") position(1,3,4,0,1) position(2,11,0,0,0) position(3,21,5,1,0) position(4,7,1,0,0) position(5,1,3,0,0) position(6,12,5,0,0) position(7,4,0,0,0) position(8,4,4,0,0)"

if __name__ == "__main__":
    # Choisir la solution à visualiser
    visualize_solution(solution_2x4x4, "2x4x4")
    # Ou pour visualiser la solution 2x2x8:
    #visualize_solution(solution_2x2x8, "2x2x8")