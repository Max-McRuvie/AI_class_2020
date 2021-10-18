import sys
import os
import csv
import numpy as np
import math
import time

# get courdinates and puts in in vector
def get_courdinates(base_arr, cave_num):
    first_courd_index = int(cave_num * 2 + 1)
    courds = np.array(base_arr[1:first_courd_index]).astype(int)
    vector_courds = []
    for i in range(0,first_courd_index-1):
        if (i % 2 == 0):
            vector_courds.append((courds[i], courds[i+1]))
    return vector_courds

# get connections, puts them in array
def get_connections(base_arr, courds, cave_num):
    first_connection_index = int(cave_num * 2 + 1) # Gets multiple of 
    con = base_arr[first_connection_index:len(base_arr)]
    return con

# creates matrix, then replaces 1's in it with the corrosponding 
# uclid distance
def matrix(connections, cave_num, courds):
    connection_matrix = []

    for i in range(cave_num): # creating base matrix
        connection_matrix.append(connections[i*cave_num:i*cave_num+cave_num])

    connection_matrix_with_uclidiandistance = []

    for i in range(len(connection_matrix)): # creating matrix with 1's replaced with uclid
        cave = []
        total = 0
        for k in range(len(connection_matrix[i])):
            if(connection_matrix[i][k] == 1):
                cave.append(uclid(courds[i], courds[k])) # uclid
                total += uclid(courds[i], courds[k])
            else:
                cave.append(0)
        connection_matrix_with_uclidiandistance.append(cave)    
    return connection_matrix_with_uclidiandistance

# gets uclid distance
def uclid(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)


class Node():

    def __init__(self,parent=None, position=None): # initialize Node
        self.parent = parent
        self.position = position

        self.f = 0
        self.g = 0
        self.h = 0

class Astar:

    def __init__(self, connections, courds, start_cave, end_cave): # initialize Astar
        self.cave_connections_matrix = connections
        self.cave_courds_array = courds

        self.start_node = Node(None, start_cave)
        self.start_node.g = self.start_node.h = self.start_node.f = 0

        self.end_node = Node(None, end_cave)
        self.end_node.g = self.end_node.h = self.end_node.f = 0

        self.open_list = []
        self.closed_list = []

        self.open_list.append(self.start_node)
    
    # runs a star
    def run(self):
        path = self.a_star_algorithm() 
        distance = 0
        for index, cave in enumerate(path): # checks path allowed & gets distance of path taken
            if (index + 1) < len(path):         
                next_cave = path[index+1]
                cons_dist = self.cave_connections_matrix[cave-1][next_cave-1]
                if(cons_dist > 0 ) : 
                    distance = distance + cons_dist
                else:
                    return None, None, None
        return distance, path

    # gets heuristics
    def heuristic(self, current_cave, end_cave):
      current_cave_cords = self.cave_courds_array[current_cave]
      end_cave_courds = self.cave_courds_array[end_cave]
      distance_between_current_and_end = uclid(current_cave_cords, end_cave_courds)

      return distance_between_current_and_end*2
      
    # the a star algorithm
    def a_star_algorithm(self):
        while len(self.open_list) > 0:
            current_node = self.open_list[0]
            current_index = 0

            for index, item in enumerate(self.open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # pop current off open list, add to closed list
            self.open_list.pop(current_index)
            self.closed_list.append(current_node)

             # found the goal
            if current_node.position == self.end_node.position:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1] # Return reversed path

            # generate children 
            children = []
            for index_position, new_position_dist in enumerate(self.cave_connections_matrix[current_node.position-1]): # Adjacent squares

                if(new_position_dist == 0): continue
                # get node position
                node_position = index_position + 1
                # greate new node
                new_node = Node(current_node, node_position)
                # distance betwwen new node and start
                new_node.g = current_node.g + new_position_dist
                # heuristic
                new_node.h = self.heuristic(index_position, len(self.cave_courds_array) - 1)
                # total node cost
                new_node.f = new_node.g + new_node.h
                # Append
                children.append(new_node)
            
            # Loop through children
            for child in children:
                
                # Child is on the closed list
                for closed_child in self.closed_list:
                    if child == closed_child:
                        continue

                # Child is already in the open list
                for open_node in self.open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                self.open_list.append(child)

# main
def main():
    console_input = sys.argv
    file_name = str(console_input[1]) + ".cav"
    

    base_arr=[] # this is base array
    temp_arr=[]

    # opens file
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for base_arr in reader:
            temp_arr.append(base_arr)

    cave_num = int(base_arr[0]) # gets num of caves

    # runs functions
    courds = get_courdinates(base_arr, cave_num)
    connections = get_connections(base_arr, courds, cave_num)
    con_martix = matrix(connections, cave_num, courds)

    # runs algorithm
    A = Astar(con_martix, courds, 1, cave_num)
    distance, path = A.run()

    # below outputs file
    path_output = ""

    if distance != None or path != None :
        for cave in path:
          path_output = path_output + ' ' + str(cave)
    else:
        output = 'No path could be found.'
    
    with open("solution.csn","w+") as f:
        f.write(path_output)

if __name__ == "__main__":
    main()
