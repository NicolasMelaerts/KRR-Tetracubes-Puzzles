% Definition of a 2x2x8 grid
width(0..7).
height(0..1).
depth(0..1).
cell(X,Y,Z) :- width(X), height(Y), depth(Z).

% Constants
#const total_cells = 32.
#const num_tetracubes = 8.

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

% Fixed assignment of types to IDs
assignType(1, "I").
assignType(2, "T").
assignType(3, "L").
assignType(4, "Pyramid").
assignType(5, "O").
assignType(6, "N").
assignType(7, "Z").
assignType(8, "Z_mirror").

% Choosing the position and rotation for each tetracube
% Only use valid orientations for each tetracube type
1 { position(P, R, X, Y, Z) : width(X), height(Y), depth(Z), validOrientation(Type, R) } 1 :- 
    tetracubeID(P), assignType(P, Type).

% Placing tetracubes on the grid
occupied(P, X+DX, Y+DY, Z+DZ) :- position(P, R, X, Y, Z), assignType(P, Type), 
                                cube(Type, R, DX, DY, DZ).

% Ensure tetracubes stay within grid limits
:- position(P, R, X, Y, Z), assignType(P, Type), cube(Type, R, DX, DY, DZ), 
   not width(X+DX).
:- position(P, R, X, Y, Z), assignType(P, Type), cube(Type, R, DX, DY, DZ), 
   not height(Y+DY).
:- position(P, R, X, Y, Z), assignType(P, Type), cube(Type, R, DX, DY, DZ), 
   not depth(Z+DZ).

% Prevent overlapping tetracubes
:- occupied(P1, X, Y, Z), occupied(P2, X, Y, Z), P1 != P2.

% Ensure all cells are occupied
cellOccupied(X, Y, Z) :- occupied(P, X, Y, Z), tetracubeID(P).
:- cell(X, Y, Z), not cellOccupied(X, Y, Z).

% Include tetracube definitions
#include "tetracubes.lp".

% Display solution
#show position/5.
#show assignType/2.
