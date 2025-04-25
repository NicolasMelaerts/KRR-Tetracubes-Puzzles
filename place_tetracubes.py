import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from matplotlib.widgets import Button, RadioButtons
from draw_tetracubes import get_all_rotations
import re

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
    def __init__(self, puzzle_solution, full_solution, cube_type="2x4x4"):
        self.puzzle_solution = puzzle_solution
        self.full_solution = full_solution
        self.current_solution = puzzle_solution  # Start with puzzle view
        self.cube_type = cube_type
        self.two_grids = False  # Initialize two_grids to False by default
        
        # Set dimensions based on cube type
        if cube_type == "2x2x8":
            self.width = 8
            self.height = 2
            self.depth = 2
        elif cube_type == "2x2x4x2":  # Two 2x2x4 grids
            self.width = 4
            self.height = 2
            self.depth = 2
            self.two_grids = True
        else:  # Default to 2x4x4
            self.width = 4
            self.height = 4
            self.depth = 2
        
        # Parse both solutions
        self.parse_solution()
        
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
        if self.two_grids:
            self.fig = plt.figure(figsize=(16, 8))
            self.ax1 = self.fig.add_subplot(121, projection='3d')
            self.ax2 = self.fig.add_subplot(122, projection='3d')
            self.axes = [self.ax1, self.ax2]
        else:
            self.fig = plt.figure(figsize=(12, 10))
            self.ax = self.fig.add_subplot(111, projection='3d')
            self.axes = [self.ax]
        
        # Current number of tetracubes to display (0 to start)
        self.num_tetracubes = 0
        self.max_tetracubes = len(self.assign_type)
        
        # Get sorted tetracube IDs
        self.tetracube_ids = sorted(self.assign_type.keys())
        
        # Store tetracube collections
        self.tetracube_collections = {}
        
        # Create buttons for navigation
        self.ax_prev = plt.axes([0.7, 0.05, 0.1, 0.075])
        self.ax_next = plt.axes([0.81, 0.05, 0.1, 0.075])
        self.btn_prev = Button(self.ax_prev, 'Previous')
        self.btn_next = Button(self.ax_next, 'Next')
        self.btn_prev.on_clicked(self.prev_tetracube)
        self.btn_next.on_clicked(self.next_tetracube)
        
        # Create radio buttons for puzzle/solution toggle
        self.ax_radio = plt.axes([0.025, 0.05, 0.15, 0.15])
        self.radio = RadioButtons(self.ax_radio, ('Puzzle', 'Solution'))
        self.radio.on_clicked(self.toggle_view)
        
        # Initialize the plot
        self.update_plot()
    
    def parse_solution(self):
        """Parse both puzzle and full solution."""
        # Initialize data structures
        self.assign_type = {}
        self.positions = {}
        self.piece_grid = {}
        
        # Parse the current solution
        solution = self.current_solution
        
        # Extract piece types
        for item in solution.split():
            if item.startswith("assignType"):
                match = re.match(r'assignType\((\d+),"([^"]+)"\)', item)
                if match:
                    piece_id = int(match.group(1))
                    piece_type = match.group(2)
                    self.assign_type[piece_id] = piece_type
            
            # Extract positions for grid_type 1 and 2
            elif item.startswith("position") and "," in item and not item.endswith(","):
                if len(item.split(",")) == 5:  # position(P,R,X,Y,Z)
                    match = re.match(r'position\((\d+),(\d+),(\d+),(\d+),(\d+)\)', item)
                    if match:
                        piece_id = int(match.group(1))
                        rotation = int(match.group(2))
                        x = int(match.group(3))
                        y = int(match.group(4))
                        z = int(match.group(5))
                        self.positions[piece_id] = (rotation, x, y, z)
                
                # Extract positions for grid_type 3
                elif len(item.split(",")) == 6:  # position(P,R,X,Y,Z,G)
                    match = re.match(r'position\((\d+),(\d+),(\d+),(\d+),(\d+),(\d+)\)', item)
                    if match:
                        piece_id = int(match.group(1))
                        rotation = int(match.group(2))
                        x = int(match.group(3))
                        y = int(match.group(4))
                        z = int(match.group(5))
                        grid = int(match.group(6))
                        self.positions[piece_id] = (rotation, x, y, z, grid)
                        self.piece_grid[piece_id] = grid
            
            # Extract grid assignments for grid_type 3
            elif item.startswith("pieceGrid"):
                match = re.match(r'pieceGrid\((\d+),(\d+)\)', item)
                if match:
                    piece_id = int(match.group(1))
                    grid = int(match.group(2))
                    self.piece_grid[piece_id] = grid
        
        # Update max_tetracubes and tetracube_ids
        self.max_tetracubes = len(self.assign_type)
        self.tetracube_ids = sorted(self.assign_type.keys())
    
    def toggle_view(self, label):
        """Toggle between puzzle and solution view."""
        if label == 'Puzzle':
            self.current_solution = self.puzzle_solution
            # Count the number of pieces in the puzzle
            piece_count = 0
            for item in self.puzzle_solution.split():
                if item.startswith("position"):
                    piece_count += 1
            self.num_tetracubes = piece_count
        else:  # Solution
            self.current_solution = self.full_solution
            # Show all pieces for the solution
            self.num_tetracubes = self.max_tetracubes
        
        # Parse the new solution
        self.parse_solution()
        
        # Update the plot
        self.update_plot()
    
    def prev_tetracube(self, event):
        """Show one less tetracube."""
        if self.num_tetracubes > 0:
            self.num_tetracubes -= 1
            self.update_plot()
    
    def next_tetracube(self, event):
        """Show one more tetracube."""
        if self.num_tetracubes < self.max_tetracubes:
            self.num_tetracubes += 1
            self.update_plot()
    
    def update_plot(self):
        # Clear the plot
        if self.two_grids:
            for ax in self.axes:
                ax.clear()
                
            # Set labels and limits for both axes
            for i, ax in enumerate(self.axes):
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                ax.set_xlim([0, self.width])
                ax.set_ylim([0, self.height])
                ax.set_zlim([0, self.depth])
                
                # Draw grid lines
                for i in range(self.width + 1):
                    for j in range(self.height + 1):
                        ax.plot([i, i], [j, j], [0, self.depth], 'k-', alpha=0.1)
                        
                for i in range(self.width + 1):
                    for k in range(self.depth + 1):
                        ax.plot([i, i], [0, self.height], [k, k], 'k-', alpha=0.1)
                        
                for j in range(self.height + 1):
                    for k in range(self.depth + 1):
                        ax.plot([0, self.width], [j, j], [k, k], 'k-', alpha=0.1)
        else:
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
        
        # Determine if we're showing puzzle or solution
        view_mode = "Puzzle" if self.current_solution == self.puzzle_solution else "Solution"
        
        if self.two_grids:
            self.axes[0].legend(handles=legend_elements, loc='upper right')
            self.axes[0].set_title(f"Grid 1 - {view_mode} - {self.num_tetracubes}/{self.max_tetracubes}")
            self.axes[1].set_title(f"Grid 2 - {view_mode} - {self.num_tetracubes}/{self.max_tetracubes}")
        else:
            self.ax.legend(handles=legend_elements, loc='upper right')
            # Add counter
            plt.title(f"{title} - {view_mode} ({self.num_tetracubes}/{self.max_tetracubes})")
            
        plt.tight_layout()
        self.fig.canvas.draw_idle()
    
    def draw_tetracube(self, id_num):
        type_name = self.assign_type[id_num]
        color = self.colors[type_name]
        
        if self.two_grids:
            if id_num in self.positions and len(self.positions[id_num]) == 5:
                rotation_id, x, y, z, grid = self.positions[id_num]
                ax_index = grid - 1  # Grid 1 -> index 0, Grid 2 -> index 1
            elif id_num in self.positions and id_num in self.piece_grid:
                rotation_id, x, y, z = self.positions[id_num]
                grid = self.piece_grid[id_num]
                ax_index = grid - 1
            else:
                print(f"Warning: Missing grid information for tetracube {id_num}")
                return
                
            ax = self.axes[ax_index]
        else:
            if id_num in self.positions:
                if len(self.positions[id_num]) == 4:  # (rotation, x, y, z)
                    rotation_id, x, y, z = self.positions[id_num]
                else:  # Ignore grid information if not in two_grids mode
                    rotation_id, x, y, z = self.positions[id_num][:4]
            else:
                print(f"Warning: Missing position for tetracube {id_num}")
                return
                
            ax = self.ax
        
        # Get the tetracube shape based on rotation
        if type_name in all_rotations and 0 <= rotation_id-1 < len(all_rotations[type_name]):
            shape = all_rotations[type_name][rotation_id-1]
            
            # Draw each cube in the tetracube
            cubes = []
            for dx, dy, dz in shape:
                cube = draw_cube(ax, (x + dx, y + dy, z + dz), color)
                cubes.append(cube)
            
            self.tetracube_collections[id_num] = cubes
        else:
            print(f"Warning: Tetracube {type_name} with rotation {rotation_id} not found")
    
    def show(self):
        plt.show()

def extract_models_from_file(filename):
    """Extract puzzle and solution models from a file."""
    with open(filename, 'r') as f:
        content = f.read()
    
    # Find all answer sets
    match = re.search(r'Answer: \d+\n(.*?)\n', content, re.DOTALL)
    if not match:
        return None, None
    
    answer = match.group(1).strip()
    
    # Create puzzle and solution from the same answer
    puzzle_solution = answer.replace("hintPosition", "position")
    full_solution = answer.replace("fullPosition", "position")
    
    return puzzle_solution, full_solution

def detect_grid_type(solution):
    """Détecte automatiquement le type de grille à partir de la solution."""
    if "pieceGrid" in solution:
        return "2x2x4x2"  # Deux grilles 2x2x4
    
    # Analyser les positions pour déterminer les dimensions
    max_x = 0
    max_y = 0
    
    for item in solution.split():
        if item.startswith("position"):
            parts = item.replace("position(", "").replace(")", "").split(",")
            if len(parts) >= 5:  # Assurez-vous qu'il y a assez de parties
                x = int(parts[2])
                y = int(parts[3])
                max_x = max(max_x, x)
                max_y = max(max_y, y)
    
    if max_x >= 4:  # Si x va jusqu'à 4 ou plus, c'est probablement 2x2x8
        return "2x2x8"
    elif max_y >= 3:  # Si y va jusqu'à 3 ou plus, c'est probablement 2x4x4
        return "2x4x4"
    else:
        # Par défaut, si on ne peut pas déterminer
        return "2x4x4"

def visualize_solution_from_file(filename):
    """Visualise une solution à partir d'un fichier."""
    puzzle_solution, full_solution = extract_models_from_file(filename)
    
    if puzzle_solution and full_solution:
        grid_type = detect_grid_type(full_solution)
        print(f"Detected grid type: {grid_type}")
        visualizer = SolutionVisualizer(puzzle_solution, full_solution, grid_type)
        visualizer.show()
    elif puzzle_solution:  # If we only have puzzle
        grid_type = detect_grid_type(puzzle_solution)
        print(f"Detected grid type: {grid_type}")
        print("Warning: Only puzzle found, using it as both puzzle and solution")
        visualizer = SolutionVisualizer(puzzle_solution, puzzle_solution, grid_type)
        visualizer.show()
    elif full_solution:  # If we only have solution
        grid_type = detect_grid_type(full_solution)
        print(f"Detected grid type: {grid_type}")
        print("Warning: Only solution found, using it as both puzzle and solution")
        visualizer = SolutionVisualizer(full_solution, full_solution, grid_type)
        visualizer.show()
    else:
        print("Could not find any valid models in the file.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Si un fichier est spécifié en argument
        visualize_solution_from_file(sys.argv[1])
    else:
        # Sinon, afficher un message d'aide
        print("No solution file specified.")
        print("Usage: python place_tetracubes.py solution.txt")
        print("To generate a solution file, run:")
        print("clingo ASP_codes/BIG_CUBE_PUZZLE.lp -c grid_type=1 --models=2 > solution.txt")