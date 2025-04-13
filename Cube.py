import numpy as np
import copy

class cube:

    #dim is the side length of the cube, measured in minicubes, and parts
    #is a list of lists of tuples, where each internal list is representative
    #of a single part and its minicube constituents.
    def __init__(self, dim, parts):
        #declares a dim x dim x dim list of zeros
        self.dim = dim
        self.cube_arr = [[[0 for width in range(dim)]for depth in range(dim)] for height in range(dim)]
        parts_list = []

        for p in parts:
            parts_list.append(part(p))
            
        self.sorted_parts = sorted(parts_list, key=lambda p: len(p.mini_cubes), reverse=True)
        print("Cube Initialization Finished")


    def solve(self, unplaced):
        if len(unplaced) == 0:
            return True
        
        p = unplaced[0]
        isplaced = False

        for x in range(self.dim):
            for y in range(self.dim):
                for z in range(self.dim):
                    for orientation in p.orientations:
                        isvalid = False
                        if self.valid_place(orientation, (x, y, z)):
                            self.place_piece(orientation, (x, y, z), p.part_number)
                            isvalid = self.solve(unplaced[1:])
                            if not isvalid:
                                self.place_piece(orientation, (x, y, z), 0)
                            else:
                                return True
        
        return False


    def place_piece(self, _part, xyz, part_number):
        for mini_cube in _part:
            self.cube_arr[mini_cube[0] + xyz[0]][mini_cube[1] + xyz[1]][mini_cube[2] + xyz[2]] = part_number


    def valid_place(self, _part, xyz):
        for mini_cube in _part:
            #Check if mini_cube is in bounds
            minipos = [mini_cube[0] + xyz[0], mini_cube[1] + xyz[1], mini_cube[2] + xyz[2]]
            if (minipos[0]) not in range(self.dim) or (minipos[1]) not in range(self.dim) or (minipos[2]) not in range(self.dim) or (self.cube_arr[minipos[0]][minipos[1]][minipos[2]]) != 0:
                return False
        return True


    def __str__(self):
        print("Parts list:")
        for p in self.sorted_parts:
            print(f"Part # {p.part_number} - {p.mini_cubes}")

        print("-------------------------------------------------------------------------------------------")

        print("XZ-Plane Views")
        print("=======================================================")
        

        for i in range(self.dim):
            for j in range(self.dim):
                print(self.cube_arr[i][j])
            print("=======================================================")
        
        return ""


            
class part:

    num_parts = 1

    #arr is an array of tuples, (x, y, z), representing the relative
    #locations of all minicubes in the part in relation to the anchor
    #minicube (0, 0, 0)
    #orientations is a list of lists of tuples. each inner list acts as a different orientation of the part
    def __init__(self, arr):
        self.mini_cubes = arr
        self.orientations = self.orientations()
        self.part_number = part.num_parts
        part.num_parts += 1

    def orientations(self):
        #using a composition of 0-3 of each of the rotation transform matrices, you can reach any of the possible position
        rotxz = np.array([[0, 0, -1],
                          [0, 1, 0],
                          [1, 0, 0]])
        
        rotyz = np.array([[1, 0, 0],
                          [0, 0, -1],
                          [0, 1, 0]])
        
        rotxy = np.array([[0, 1, 0],
                          [-1, 0, 0],
                          [0, 0, 1]])
        
        orients = []

        #each of the main for loops loops through 0 - 3 and rotates the part 90 degrees in that plane that many times.
        for xz in range(4):
            final_mat = np.array([[1,0,0],[0,1,0],[0,0,1]])
            for i in range(xz):
                final_mat = np.matmul(rotxz, final_mat)
            
            for yz in range(4):
                for i in range(yz):
                    final_mat = np.matmul(rotyz, final_mat)

                for xy in range(4):
                    for i in range(xy):
                        final_mat = np.matmul(rotxy, final_mat)
                        temp_part = []

                        for mini_cube in self.mini_cubes:
                            temp_part.append(np.matmul(np.array(mini_cube), final_mat))
                        orients.append(temp_part)
        
        output = part.remove_dupes(orients)

        print(f"Done Orienting part {self.part_number}")
        return output

    #takes a list of orientations and removes all duplicate orientations
    def remove_dupes(orientations):
        tempO = copy.copy(orientations)

        set_list = []
        i = 0
        while i < len(tempO):
            popped = False
            set1 = set()
            for mini_cube in tempO[i]:
                set1.add(tuple(mini_cube))
            for s in set_list:
                if len(s.difference(set1)) == 0:
                    tempO.pop(i)
                    popped = True
                    break
                    
            if not popped:
                set_list.append(set1)
                i += 1

            if len(set_list) == 0:
                set_list.append(set1)

            
        return tempO

        

def main():
    ps = [ 
        [(0,0,0),(0,1,0),(1,1,0),(0,2,0),(1,2,0),(2,2,0),(2,2,1)],
        [(0,0,0),(-1,0,0),(-1,1,0),(-2,1,0),(-2,1,1)],
        [(0,0,0),(0,1,0),(-1,1,0),(-2,1,0),(-3,1,0),(-3,2,0)],
        [(0,0,0),(0,-1,0),(-1,-1,0),(-1,-1,1),(-2,-1,0),(-3,-1,0),(-3,0,0),(-3,0,1)],
        [(0,0,0),(1,0,0),(1,1,0),(1,1,1),(2,1,1)],
        [(0,0,0),(-1,0,0),(-2,0,0),(-2,1,0),(-3,1,0)],
        [(0,0,0),(0,1,0),(-1,1,0),(-1,1,1)],
        [(0,0,0),(-1,0,0),(-2,0,0),(-2,1,0),(-2,1,1),(-3,1,1)],
        [(0,0,0),(1,0,0),(1,1,0),(1,1,1),(2,0,0)],
        [(0,0,0),(-1,1,0),(0,1,0),(1,1,0),(1,1,1),(1,2,1)],
        [(0,0,0),(0,0,1),(1,0,0),(2,0,0),(2,-1,0),(2,-1,1),(3,0,0)]
     ]
    c1 = cube(4, ps)
    print(c1)
    print("Solving... This may take a while")
    c1.solve(c1.sorted_parts)
    print("Solved!!!")
    print("-------------------------------------------------------------")
    print(c1)

main()