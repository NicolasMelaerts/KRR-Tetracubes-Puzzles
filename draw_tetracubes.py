import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

def draw_cube(coords, ax, color='b'):
    for x, y, z in coords:
        vertices = [
            [(x, y, z), (x+1, y, z), (x+1, y+1, z), (x, y+1, z)],
            [(x, y, z+1), (x+1, y, z+1), (x+1, y+1, z+1), (x, y+1, z+1)],
            [(x, y, z), (x, y, z+1), (x, y+1, z+1), (x, y+1, z)],
            [(x+1, y, z), (x+1, y, z+1), (x+1, y+1, z+1), (x+1, y+1, z)],
            [(x, y, z), (x+1, y, z), (x+1, y, z+1), (x, y, z+1)],
            [(x, y+1, z), (x+1, y+1, z), (x+1, y+1, z+1), (x, y+1, z+1)]
        ]
        ax.add_collection3d(Poly3DCollection(vertices, facecolors=color, linewidths=0.5, edgecolors='k'))

def visualize_cubes(cube_list):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    colors = ['b', 'r', 'g', 'y', 'c', 'm']
    
    for i, (coords, color) in enumerate(zip(cube_list, colors)):
        draw_cube(coords, ax, color)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim([-1, 5])
    ax.set_ylim([-1, 5])
    ax.set_zlim([-1, 5])
    plt.show()

def visualize_tetracubes_one_by_one(tetracubes):
    """Display tetracubes one at a time with navigation controls."""
    from matplotlib.widgets import Button
    
    current_index = [0]  # Using a list to allow modification inside nested functions
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    def update_plot():
        ax.clear()
        tetracube = tetracubes[current_index[0]]
        draw_cube(tetracube, ax, color='b')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim([-1, 5])
        ax.set_ylim([-1, 5])
        ax.set_zlim([-1, 5])
        ax.set_title(f'Tetracube {current_index[0]+1} of {len(tetracubes)}')
        fig.canvas.draw_idle()
    
    def on_next(event):
        current_index[0] = (current_index[0] + 1) % len(tetracubes)
        update_plot()
    
    def on_prev(event):
        current_index[0] = (current_index[0] - 1) % len(tetracubes)
        update_plot()
    
    # Add buttons for navigation
    ax_prev = plt.axes([0.7, 0.05, 0.1, 0.075])
    ax_next = plt.axes([0.81, 0.05, 0.1, 0.075])
    btn_prev = Button(ax_prev, 'Previous')
    btn_next = Button(ax_next, 'Next')
    btn_prev.on_clicked(on_prev)
    btn_next.on_clicked(on_next)
    
    update_plot()  # Initial plot
    plt.show()

def generate_adjacent_cubes(base_cube):
    directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    new_cubes = []
    
    for cube in base_cube:
        for dx, dy, dz in directions:
            new_pos = (cube[0] + dx, cube[1] + dy, cube[2] + dz)
            if new_pos not in base_cube:
                new_cube = base_cube.copy()
                new_cube.append(new_pos)
                new_cubes.append(new_cube)
    
    # Remove duplicates
    unique_cubes = []
    for cube in new_cubes:
        sorted_cube = sorted(cube)
        if sorted_cube not in [sorted(c) for c in unique_cubes]:
            unique_cubes.append(cube)
    
    return unique_cubes

def generate_tetracubes():
    # Start with a single cube
    monomino = [(0, 0, 0)]
    
    # Generate dominos (2 cubes)
    dominos = generate_adjacent_cubes(monomino)
    
    # Generate trominos (3 cubes)
    trominos = []
    for domino in dominos:
        trominos.extend(generate_adjacent_cubes(domino))
    
    # Generate tetrominos (4 cubes)
    tetracubes = []
    for tromino in trominos:
        tetracubes.extend(generate_adjacent_cubes(tromino))
    
    return tetracubes

def normalize_polyomino(polyomino):
    """Normalize a polyomino by translating it so that min x,y,z is at origin."""
    min_x = min(x for x, y, z in polyomino)
    min_y = min(y for x, y, z in polyomino)
    min_z = min(z for x, y, z in polyomino)
    return [(x-min_x, y-min_y, z-min_z) for x, y, z in polyomino]

def get_all_rotations(polyomino):
    """Get all 24 possible 3D rotations of a polyomino."""
    rotations = []
    
    # Define the 24 rotation matrices for a cube
    rot_matrices = []
    
    # Rotations around x, y, z axes (90, 180, 270 degrees)
    for axis in range(3):  # 0=x, 1=y, 2=z
        for angle in range(4):  # 0, 90, 180, 270 degrees
            matrix = np.identity(3)
            if angle > 0:
                # Create rotation matrix
                if axis == 0:  # x-axis
                    c, s = np.cos(angle * np.pi/2), np.sin(angle * np.pi/2)
                    matrix = np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
                elif axis == 1:  # y-axis
                    c, s = np.cos(angle * np.pi/2), np.sin(angle * np.pi/2)
                    matrix = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
                elif axis == 2:  # z-axis
                    c, s = np.cos(angle * np.pi/2), np.sin(angle * np.pi/2)
                    matrix = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
            rot_matrices.append(matrix)
    
    # Add the remaining orientations to get all 24
    # These are the 24 ways to orient a cube in 3D space
    orientations = [
        [1, 2, 3], [1, 3, -2], [1, -2, -3], [1, -3, 2],
        [-1, 2, -3], [-1, -3, -2], [-1, -2, 3], [-1, 3, 2],
        [2, 1, -3], [2, -3, -1], [2, -1, 3], [2, 3, 1],
        [-2, 1, 3], [-2, 3, -1], [-2, -1, -3], [-2, -3, 1],
        [3, 1, 2], [3, 2, -1], [3, -1, -2], [3, -2, 1],
        [-3, 1, -2], [-3, -2, -1], [-3, -1, 2], [-3, 2, 1]
    ]
    
    # Apply each rotation
    for orientation in orientations:
        rotated = []
        for x, y, z in polyomino:
            # Apply the orientation
            rx, ry, rz = 0, 0, 0
            if abs(orientation[0]) == 1:
                rx = x * orientation[0]
            elif abs(orientation[0]) == 2:
                rx = y * (orientation[0] // 2)
            else:
                rx = z * (orientation[0] // 3)
                
            if abs(orientation[1]) == 1:
                ry = x * orientation[1]
            elif abs(orientation[1]) == 2:
                ry = y * (orientation[1] // 2)
            else:
                ry = z * (orientation[1] // 3)
                
            if abs(orientation[2]) == 1:
                rz = x * orientation[2]
            elif abs(orientation[2]) == 2:
                rz = y * (orientation[2] // 2)
            else:
                rz = z * (orientation[2] // 3)
                
            rotated.append((rx, ry, rz))
        
        # Normalize the rotated polyomino
        rotated = normalize_polyomino(rotated)
        rotated = sorted(rotated)
        
        if rotated not in rotations:
            rotations.append(rotated)
    
    return rotations

def get_canonical_form(polyomino):
    """Get the canonical form of a polyomino (lexicographically smallest among all rotations)."""
    all_rotations = get_all_rotations(polyomino)
    return min(all_rotations)

def categorize_tetracubes(tetracubes):
    """Categorize tetracubes into free and unilateral forms."""
    free_forms = []  # Distinct shapes (ignoring reflections)
    unilateral_forms = []  # Distinct shapes (counting reflections as different)
    
    for tetracube in tetracubes:
        # Normalize and sort the tetracube
        normalized = normalize_polyomino(tetracube)
        normalized = sorted(normalized)
        
        # Get canonical form
        canonical = get_canonical_form(normalized)
        
        # Check if this is a new free form
        if not any(np.array_equal(canonical, existing) for existing in free_forms):
            free_forms.append(canonical)
            
        # Check if this is a new unilateral form
        if not any(np.array_equal(normalized, existing) for existing in unilateral_forms):
            unilateral_forms.append(normalized)
    
    return {
        'free': free_forms,  # Should be 7
        'unilateral': unilateral_forms  # Should be 8
    }

def visualize_tetracubes_by_category(categorized_tetracubes):
    """Display tetracubes by category with navigation controls."""
    from matplotlib.widgets import Button, RadioButtons
    
    # Setup figure and axes
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Current state
    current_state = {
        'category': 'free',
        'index': 0
    }
    
    def update_plot():
        ax.clear()
        category = current_state['category']
        index = current_state['index']
        tetracubes = categorized_tetracubes[category]
        
        if tetracubes:
            tetracube = tetracubes[index]
            print(tetracube)
            draw_cube(tetracube, ax, color='b')
            ax.set_title(f'{category.capitalize()} Tetracube {index+1} of {len(tetracubes)}')
        else:
            ax.set_title(f'No tetracubes in {category} category')
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim([-1, 5])
        ax.set_ylim([-1, 5])
        ax.set_zlim([-1, 5])
        fig.canvas.draw_idle()
    
    def on_next(event):
        category = current_state['category']
        tetracubes = categorized_tetracubes[category]
        if tetracubes:
            current_state['index'] = (current_state['index'] + 1) % len(tetracubes)
            update_plot()
    
    def on_prev(event):
        category = current_state['category']
        tetracubes = categorized_tetracubes[category]
        if tetracubes:
            current_state['index'] = (current_state['index'] - 1) % len(tetracubes)
            update_plot()
    
    def on_category_change(label):
        current_state['category'] = label.lower()
        current_state['index'] = 0
        update_plot()
    
    # Add navigation buttons
    ax_prev = plt.axes([0.7, 0.05, 0.1, 0.075])
    ax_next = plt.axes([0.81, 0.05, 0.1, 0.075])
    btn_prev = Button(ax_prev, 'Previous')
    btn_next = Button(ax_next, 'Next')
    btn_prev.on_clicked(on_prev)
    btn_next.on_clicked(on_next)
    
    # Add category radio buttons
    ax_radio = plt.axes([0.05, 0.05, 0.15, 0.15])
    radio = RadioButtons(ax_radio, ('Free', 'Unilateral'))
    radio.on_clicked(on_category_change)
    
    update_plot()  # Initial plot
    plt.show()

def visualize_all_tetracubes_together(categorized_tetracubes, category='free'):
    """Display all tetracubes together in a grid layout."""
    tetracubes = categorized_tetracubes[category]
    n = len(tetracubes)
    
    # Determine grid dimensions
    grid_size = int(np.ceil(np.sqrt(n)))
    
    fig = plt.figure(figsize=(15, 15))
    
    # Calculate spacing between subplots
    spacing = 0.1
    grid_width = (1.0 - spacing * (grid_size + 1)) / grid_size
    
    for i, tetracube in enumerate(tetracubes):
        # Calculate grid position
        row = i // grid_size
        col = i % grid_size
        
        # Calculate subplot position
        left = spacing + col * (grid_width + spacing)
        bottom = 1.0 - spacing - (row + 1) * (grid_width + spacing)
        
        # Create 3D subplot
        ax = fig.add_axes([left, bottom, grid_width, grid_width], projection='3d')
        
        # Draw the tetracube
        if category == 'I': 
            draw_cube(tetracube, ax, color='b')
        elif category == 'T':
            draw_cube(tetracube, ax, color='r')
        elif category == 'L':
            draw_cube(tetracube, ax, color='g')
        elif category == 'Pyramid':
            draw_cube(tetracube, ax, color='y')
        elif category == 'O':
            draw_cube(tetracube, ax, color='c')
        elif category == 'N':
            draw_cube(tetracube, ax, color='m')
        elif category == 'Z':
            draw_cube(tetracube, ax, color='cyan')
        elif category == 'Z_mirror':
            draw_cube(tetracube, ax, color='orange')
            
        
        # Set labels and limits
        ax.set_title(f'{category.capitalize()} #{i+1}')
        ax.set_xlabel('X', labelpad=-10)
        ax.set_ylabel('Y', labelpad=-10)
        ax.set_zlabel('Z', labelpad=-10)
        
        # Set consistent view limits
        ax.set_xlim([-0.5, 3.5])
        ax.set_ylim([-0.5, 3.5])
        ax.set_zlim([-0.5, 3.5])
        
        # Set consistent viewing angle
        ax.view_init(elev=30, azim=30)
        
        # Remove tick labels to reduce clutter
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])
    
    plt.suptitle(f'All {n} {category.capitalize()} Tetracubes', fontsize=16)
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.show()


if __name__ == "__main__":
    # Generate all tetracubes
    tetracubes = generate_tetracubes()
    print(f"Number of tetracubes generated: {len(tetracubes)}")

    # Categorize tetracubes
    categorized_tetracubes = categorize_tetracubes(tetracubes)
    print(f"Number of free tetracubes: {len(categorized_tetracubes['free'])}")
    print(f"Number of unilateral tetracubes: {len(categorized_tetracubes['unilateral'])}")

    # Visualize tetracubes by category
    #visualize_tetracubes_by_category(categorized_tetracubes)

    # Visualize all free tetracubes together
    #visualize_all_tetracubes_together(categorized_tetracubes, 'free')

    # Visualize all unilateral tetracubes together
    # visualize_all_tetracubes_together(categorized_tetracubes, 'unilateral')


    #print(categorized_tetracubes['free'])

    tetracube_I = [(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 0, 3)]
    tetracube_I_rotated = get_all_rotations(tetracube_I)
    print(tetracube_I_rotated)

    temp_dict = {'I': tetracube_I_rotated}
    visualize_all_tetracubes_together(temp_dict, 'I')

    tetracube_T = [(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 1)]
    tetracube_T_rotated = get_all_rotations(tetracube_T)
    print(tetracube_T_rotated)

    temp_dict = {'T': tetracube_T_rotated}
    visualize_all_tetracubes_together(temp_dict, 'T')


    tetracube_L = [(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 0)]
    tetracube_L_rotated = get_all_rotations(tetracube_L)
    print(tetracube_L_rotated)

    temp_dict = {'L': tetracube_L_rotated}
    visualize_all_tetracubes_together(temp_dict, 'L')


    tetracube_Pyramid = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0)]
    tetracube_Pyramid_rotated = get_all_rotations(tetracube_Pyramid)
    print(tetracube_Pyramid_rotated)

    temp_dict = {'Pyramid': tetracube_Pyramid_rotated}
    visualize_all_tetracubes_together(temp_dict, 'Pyramid')


    tetracube_O = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1)]
    tetracube_O_rotated = get_all_rotations(tetracube_O)
    print(tetracube_O_rotated)

    temp_dict = {'O': tetracube_O_rotated}
    visualize_all_tetracubes_together(temp_dict, 'O')

    tetracube_N = [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 2)]
    tetracube_N_rotated = get_all_rotations(tetracube_N)
    print(tetracube_N_rotated)

    temp_dict = {'N': tetracube_N_rotated}
    visualize_all_tetracubes_together(temp_dict, 'N')


    tetracube_Z = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 1, 0)]
    tetracube_Z_rotated = get_all_rotations(tetracube_Z)
    print(tetracube_Z_rotated)

    temp_dict = {'Z': tetracube_Z_rotated}
    visualize_all_tetracubes_together(temp_dict, 'Z')


    tetracube_Z_mirror = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 1)]
    tetracube_Z_mirror_rotated = get_all_rotations(tetracube_Z_mirror)
    print(tetracube_Z_mirror_rotated)

    temp_dict = {'Z_mirror': tetracube_Z_mirror_rotated}
    visualize_all_tetracubes_together(temp_dict, 'Z_mirror')

