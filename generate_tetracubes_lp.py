from draw_tetracubes import *

def generate_lp_file(filename="tetracubes.lp"):
    """Generate a .lp file with all tetracubes in the format cube("Type", rotation_id, x, y, z)."""
    with open(filename, "w") as f:
        # I tetracube
        tetracube_I = [(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 0, 3)]
        tetracube_I_rotated = get_all_rotations(tetracube_I)
        f.write("% I tetracube\n")
        for i, rotation in enumerate(tetracube_I_rotated):
            rotation_id = i + 1
            f.write(f"% Rotation {rotation_id}\n")
            for x, y, z in rotation:
                f.write(f'cube("I", {rotation_id}, {x}, {y}, {z}). ')
            f.write("\n")
        f.write("\n")
        
        # T tetracube
        tetracube_T = [(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 1)]
        tetracube_T_rotated = get_all_rotations(tetracube_T)
        f.write("% T tetracube\n")
        for i, rotation in enumerate(tetracube_T_rotated):
            rotation_id = i + 1
            f.write(f"% Rotation {rotation_id}\n")
            for x, y, z in rotation:
                f.write(f'cube("T", {rotation_id}, {x}, {y}, {z}). ')
            f.write("\n")
        f.write("\n")
        
        # L tetracube
        tetracube_L = [(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 0)]
        tetracube_L_rotated = get_all_rotations(tetracube_L)
        f.write("% L tetracube\n")
        for i, rotation in enumerate(tetracube_L_rotated):
            rotation_id = i + 1
            f.write(f"% Rotation {rotation_id}\n")
            for x, y, z in rotation:
                f.write(f'cube("L", {rotation_id}, {x}, {y}, {z}). ')
            f.write("\n")
        f.write("\n")

        # Pyramid tetracube
        tetracube_Pyramid = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0)]
        tetracube_Pyramid_rotated = get_all_rotations(tetracube_Pyramid)
        f.write("% Pyramid tetracube\n")
        for i, rotation in enumerate(tetracube_Pyramid_rotated):
            rotation_id = i + 1
            f.write(f"% Rotation {rotation_id}\n")
            for x, y, z in rotation:
                f.write(f'cube("Pyramid", {rotation_id}, {x}, {y}, {z}). ')
            f.write("\n")
        f.write("\n")
        
        # O tetracube
        tetracube_O = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1)]
        tetracube_O_rotated = get_all_rotations(tetracube_O)
        f.write("% O tetracube\n")
        for i, rotation in enumerate(tetracube_O_rotated):
            rotation_id = i + 1
            f.write(f"% Rotation {rotation_id}\n")
            for x, y, z in rotation:
                f.write(f'cube("O", {rotation_id}, {x}, {y}, {z}). ')
            f.write("\n")
        f.write("\n")   
        
        # N tetracube
        tetracube_N = [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 2)]
        tetracube_N_rotated = get_all_rotations(tetracube_N)
        f.write("% N tetracube\n")
        for i, rotation in enumerate(tetracube_N_rotated):
            rotation_id = i + 1
            f.write(f"% Rotation {rotation_id}\n")
            for x, y, z in rotation:
                f.write(f'cube("N", {rotation_id}, {x}, {y}, {z}). ')
            f.write("\n")
        f.write("\n")
        
        # Z tetracube
        tetracube_Z = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 1, 0)]
        tetracube_Z_rotated = get_all_rotations(tetracube_Z)
        f.write("% Z tetracube\n")
        for i, rotation in enumerate(tetracube_Z_rotated):
            rotation_id = i + 1
            f.write(f"% Rotation {rotation_id}\n")
            for x, y, z in rotation:
                f.write(f'cube("Z", {rotation_id}, {x}, {y}, {z}). ')
            f.write("\n")
        f.write("\n")
        
        # Z_mirror tetracube
        tetracube_Z_mirror = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 1)]
        tetracube_Z_mirror_rotated = get_all_rotations(tetracube_Z_mirror)
        f.write("% Z_mirror tetracube\n")
        for i, rotation in enumerate(tetracube_Z_mirror_rotated):
            rotation_id = i + 1
            f.write(f"% Rotation {rotation_id}\n")
            for x, y, z in rotation:
                f.write(f'cube("Z_mirror", {rotation_id}, {x}, {y}, {z}). ')
            f.write("\n")
        f.write("\n")
        

if __name__ == "__main__":
    generate_lp_file()
    print("Tetracubes LP file generated successfully!") 