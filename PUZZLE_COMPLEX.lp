% Include tetracube definitions
#include "tetracubes.lp".

% Grid type selection
#const grid_type = 1. % 1: 4x4x4, 2: 2x4x8, 3: 4x2x4 (two separate grids)
#const num_hints = 8.  % Number of pieces to show as hints
#const seed = 42.      % Seed for random selection

% Definition of grids based on grid_type
width(0..3) :- grid_type == 1.
height(0..3) :- grid_type == 1.
depth(0..3) :- grid_type == 1.

width(0..7) :- grid_type == 2.
height(0..3) :- grid_type == 2.
depth(0..1) :- grid_type == 2.

width(0..3) :- grid_type == 3.
height(0..1) :- grid_type == 3.
depth(0..3) :- grid_type == 3.

% For grid_type 3, we need to track which grid a piece is placed in
grid(1..2) :- grid_type == 3.
1 { pieceGrid(P, G) : grid(G) } 1 :- tetracubeID(P), grid_type == 3.

% Ensure balanced distribution for grid_type 3 (8 pieces per grid)
:- grid_type == 3, grid(G), #count { P : pieceGrid(P, G) } != 8.

% Define cells based on grid type
cell(X,Y,Z) :- width(X), height(Y), depth(Z), grid_type != 3.
cell(X,Y,Z,G) :- width(X), height(Y), depth(Z), grid(G), grid_type == 3.

% Constants
#const total_cells = 64.
#const num_tetracubes = 16.

% Tetracube types and their valid orientations
validOrientation("I", 1..3).
validOrientation("T", 1..12).
validOrientation("L", 1..24).
validOrientation("Pyramid", 1..8).
validOrientation("O", 1..3).
validOrientation("N", 1..12).
validOrientation("Z", 1..12).
validOrientation("Z_mirror", 1..12).

% Tetracube IDs to place
tetracubeID(1..num_tetracubes).

% Tetracube types
tetracubeType("I").
tetracubeType("T").
tetracubeType("L").
tetracubeType("Pyramid").
tetracubeType("O").
tetracubeType("N").
tetracubeType("Z").
tetracubeType("Z_mirror").

% Assignment of types to IDs (now allowing 2 of each type)
assignType(1, "I"). assignType(9, "I").
assignType(2, "T"). assignType(10, "T").
assignType(3, "L"). assignType(11, "L").
assignType(4, "Pyramid"). assignType(12, "Pyramid").
assignType(5, "O"). assignType(13, "O").
assignType(6, "N"). assignType(14, "N").
assignType(7, "Z"). assignType(15, "Z").
assignType(8, "Z_mirror"). assignType(16, "Z_mirror").

% Choosing the position and rotation for each tetracube
% For grid_type 1 and 2
1 { position(P, R, X, Y, Z) : width(X), height(Y), depth(Z), validOrientation(Type, R) } 1 :- 
    tetracubeID(P), assignType(P, Type), grid_type != 3.

% For grid_type 3 (two separate grids)
1 { position(P, R, X, Y, Z, G) : width(X), height(Y), depth(Z), validOrientation(Type, R) } 1 :- 
    tetracubeID(P), assignType(P, Type), pieceGrid(P, G), grid_type == 3.

% Placing tetracubes on the grid
% For grid_type 1 and 2
occupied(P, X+DX, Y+DY, Z+DZ) :- position(P, R, X, Y, Z), assignType(P, Type), 
                                cube(Type, R, DX, DY, DZ), grid_type != 3.

% For grid_type 3
occupied(P, X+DX, Y+DY, Z+DZ, G) :- position(P, R, X, Y, Z, G), assignType(P, Type), 
                                   cube(Type, R, DX, DY, DZ), grid_type == 3.

% Ensure tetracubes stay within grid limits
% For grid_type 1 and 2
:- position(P, R, X, Y, Z), assignType(P, Type), cube(Type, R, DX, DY, DZ), 
   not width(X+DX), grid_type != 3.
:- position(P, R, X, Y, Z), assignType(P, Type), cube(Type, R, DX, DY, DZ), 
   not height(Y+DY), grid_type != 3.
:- position(P, R, X, Y, Z), assignType(P, Type), cube(Type, R, DX, DY, DZ), 
   not depth(Z+DZ), grid_type != 3.

% For grid_type 3
:- position(P, R, X, Y, Z, G), assignType(P, Type), cube(Type, R, DX, DY, DZ), 
   not width(X+DX), grid_type == 3.
:- position(P, R, X, Y, Z, G), assignType(P, Type), cube(Type, R, DX, DY, DZ), 
   not height(Y+DY), grid_type == 3.
:- position(P, R, X, Y, Z, G), assignType(P, Type), cube(Type, R, DX, DY, DZ), 
   not depth(Z+DZ), grid_type == 3.

% Prevent overlapping tetracubes
% For grid_type 1 and 2
:- occupied(P1, X, Y, Z), occupied(P2, X, Y, Z), P1 != P2, grid_type != 3.

% For grid_type 3
:- occupied(P1, X, Y, Z, G), occupied(P2, X, Y, Z, G), P1 != P2, grid_type == 3.

% Ensure all cells are occupied
% For grid_type 1 and 2
cellOccupied(X, Y, Z) :- occupied(P, X, Y, Z), tetracubeID(P), grid_type != 3.
:- cell(X, Y, Z), not cellOccupied(X, Y, Z), grid_type != 3.

% For grid_type 3
cellOccupied(X, Y, Z, G) :- occupied(P, X, Y, Z, G), tetracubeID(P), grid_type == 3.
:- cell(X, Y, Z, G), not cellOccupied(X, Y, Z, G), grid_type == 3.

% Select exactly num_hints pieces as hints
{ hint(P) : tetracubeID(P) } num_hints.
:- not num_hints = #count { P : hint(P) }.

% Use seed for random selection
#heuristic hint(P) : tetracubeID(P). [seed@3,false]

% Show all piece assignments
#show assignType/2.

% Show positions for all pieces (solution)
#show fullPosition(P,R,X,Y,Z) : position(P,R,X,Y,Z), grid_type != 3.
#show fullPosition(P,R,X,Y,Z,G) : position(P,R,X,Y,Z,G), grid_type == 3.

% Show positions only for hint pieces (puzzle)
#show hintPosition(P,R,X,Y,Z) : position(P,R,X,Y,Z), hint(P), grid_type != 3.
#show hintPosition(P,R,X,Y,Z,G) : position(P,R,X,Y,Z,G), hint(P), grid_type == 3.

% Show which pieces are hints
#show hint/1.

% Show grid assignments only for grid_type 3
#show pieceGrid(P,G) : pieceGrid(P,G), grid_type == 3. 