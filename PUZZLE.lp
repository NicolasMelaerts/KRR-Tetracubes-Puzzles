% Include tetracube definitions
#include "tetracubes.lp".

% Grid type selection
#const grid_type = 1. % 1: 2x4x4, 2: 2x2x8, 3: 2x2x4 (two separate grids)
#const num_hints = 6.  % Number of pieces to show as hints
#const seed = 42.      % Seed for random selection

% Definition of grids based on grid_type
width(0..3) :- grid_type == 1.
height(0..3) :- grid_type == 1.
depth(0..1) :- grid_type == 1.

width(0..7) :- grid_type == 2.
height(0..1) :- grid_type == 2.
depth(0..1) :- grid_type == 2.

width(0..3) :- grid_type == 3.
height(0..1) :- grid_type == 3.
depth(0..1) :- grid_type == 3.

% For grid_type 3, we need to track which grid a piece is placed in
grid(1..2) :- grid_type == 3.
1 { typeGrid(Type, G) : grid(G) } 1 :- tetracubeType(Type), grid_type == 3.

% Ensure balanced distribution for grid_type 3 (4 pieces per grid)
:- grid_type == 3, grid(G), #count { Type : typeGrid(Type, G) } != 4.

% Define cells based on grid type
cell(X,Y,Z) :- width(X), height(Y), depth(Z), grid_type != 3.
cell(X,Y,Z,G) :- width(X), height(Y), depth(Z), grid(G), grid_type == 3.

% Constants
#const total_cells = 32.

% Tetracube types and their valid orientations
validOrientation("I", 1..3).
validOrientation("T", 1..12).
validOrientation("L", 1..24).
validOrientation("Pyramid", 1..8).
validOrientation("O", 1..3).
validOrientation("N", 1..12).
validOrientation("Z", 1..12).
validOrientation("Z_mirror", 1..12).

% Tetracube types
tetracubeType("I").
tetracubeType("T").
tetracubeType("L").
tetracubeType("Pyramid").
tetracubeType("O").
tetracubeType("N").
tetracubeType("Z").
tetracubeType("Z_mirror").

% Choosing the position and rotation for each tetracube
% For grid_type 1 and 2
1 { position(Type, R, X, Y, Z) : width(X), height(Y), depth(Z), validOrientation(Type, R) } 1 :- 
    tetracubeType(Type), grid_type != 3.

% For grid_type 3 (two separate grids)
1 { position(Type, R, X, Y, Z, G) : width(X), height(Y), depth(Z), validOrientation(Type, R) } 1 :- 
    tetracubeType(Type), typeGrid(Type, G), grid_type == 3.

% Placing tetracubes on the grid
% For grid_type 1 and 2
occupied(Type, X+DX, Y+DY, Z+DZ) :- position(Type, R, X, Y, Z), 
                                    cube(Type, R, DX, DY, DZ), grid_type != 3.

% For grid_type 3
occupied(Type, X+DX, Y+DY, Z+DZ, G) :- position(Type, R, X, Y, Z, G), 
                                       cube(Type, R, DX, DY, DZ), grid_type == 3.

% Ensure tetracubes stay within grid limits
% For grid_type 1 and 2
:- position(Type, R, X, Y, Z), cube(Type, R, DX, DY, DZ), 
   not width(X+DX), grid_type != 3.
:- position(Type, R, X, Y, Z), cube(Type, R, DX, DY, DZ), 
   not height(Y+DY), grid_type != 3.
:- position(Type, R, X, Y, Z), cube(Type, R, DX, DY, DZ), 
   not depth(Z+DZ), grid_type != 3.

% For grid_type 3
:- position(Type, R, X, Y, Z, G), cube(Type, R, DX, DY, DZ), 
   not width(X+DX), grid_type == 3.
:- position(Type, R, X, Y, Z, G), cube(Type, R, DX, DY, DZ), 
   not height(Y+DY), grid_type == 3.
:- position(Type, R, X, Y, Z, G), cube(Type, R, DX, DY, DZ), 
   not depth(Z+DZ), grid_type == 3.

% Prevent overlapping tetracubes
% For grid_type 1 and 2
:- occupied(Type1, X, Y, Z), occupied(Type2, X, Y, Z), Type1 != Type2, grid_type != 3.

% For grid_type 3
:- occupied(Type1, X, Y, Z, G), occupied(Type2, X, Y, Z, G), Type1 != Type2, grid_type == 3.

% Ensure all cells are occupied
% For grid_type 1 and 2
cellOccupied(X, Y, Z) :- occupied(Type, X, Y, Z), tetracubeType(Type), grid_type != 3.
:- cell(X, Y, Z), not cellOccupied(X, Y, Z), grid_type != 3.

% For grid_type 3
cellOccupied(X, Y, Z, G) :- occupied(Type, X, Y, Z, G), tetracubeType(Type), grid_type == 3.
:- cell(X, Y, Z, G), not cellOccupied(X, Y, Z, G), grid_type == 3.

% Select exactly num_hints pieces as hints
{ hint(Type) : tetracubeType(Type) } num_hints.
:- not num_hints = #count { Type : hint(Type) }.

% Use seed for random selection
#heuristic hint(Type) : tetracubeType(Type). [seed@3,false]

% Show all piece assignments for solution
#show fullPosition(Type,R,X,Y,Z) : position(Type,R,X,Y,Z), grid_type != 3.
#show fullPosition(Type,R,X,Y,Z,G) : position(Type,R,X,Y,Z,G), grid_type == 3.

% Show positions only for hint pieces (puzzle)
#show hintPosition(Type,R,X,Y,Z) : position(Type,R,X,Y,Z), hint(Type), grid_type != 3.
#show hintPosition(Type,R,X,Y,Z,G) : position(Type,R,X,Y,Z,G), hint(Type), grid_type == 3.

% Show which pieces are hints
#show hint/1.

% Show grid assignments only for grid_type 3
#show typeGrid(Type,G) : typeGrid(Type,G), grid_type == 3.