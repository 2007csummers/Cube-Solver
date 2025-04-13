# Cube-Solver
Solves a physical cube puzzle using a backtracking algorithm.

The main (Mega) cube is comprised of dim x dim x dim smaller (mini) cubes. These mini cubes are grouped into parts that contain at least one mini cube. These parts are then separated from one another, disassembling the Mega cube.

This algorithm puts them back together again.

Mega Cube - Contains a 3D array of integers that correspond to the locations that mini cubes can be placed. Each part has a unique identifier that acts as a placeholder in the Mega Cube array. Additionally, the cube contains a list of all the parts in the cube, sorted by volume descending.

Part - Contains an array of mini cubes represented as 3 element tuples (x, y, z). Additionally contains a unique part number and a list of lists of tuples that represents all possible orientations. in these lists of tuples is always a (0, 0, 0) tuple, representing the anchor mini cube of the part. all other mini cubes in the part are rotated around this anchor and are represented relationally to the anchor.

The bulky components of the algorithm are the orientations method and the solve method.

part.orientations(self) - This method uses three linear transformations to rotate each piece 90 degrees in either the xy, xz, or yz planes. This method returns all unique possible orientations for each given piece. 

