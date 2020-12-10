from __future__ import print_function
import csv
import math
from Queue import Queue
from Queue import heapq
import sys
class Nodes:
    
    def __init__(self,parent, start_position,end_position,size_of_map,initial_map):
        self.x = start_position[0]
        self.y = start_position[1]
        self.state = start_position
        self.parent = parent
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.cost_history = 0
        #self.end_position = end_position
        
    def position(self):
        #print(f'[{self.x},{self.y}]')
        return [self.x, self.y]
    def elevate_value(self,x,y):
        #print(x)
        #print(y)
        elevate_value = initial_map[x][y]
        #print(f'x:{x} y:{y} elevate_value:{elevate_value}')
        if elevate_value !="X":
            return int(elevate_value)
        else: 
            return elevate_value

    def euclideanDistance(self,end_position):
        vertical_distance = abs(end_position[1]-self.state[1])
        horizontal_distance = abs(end_position[0]-self.state[0])
        return math.sqrt(pow(vertical_distance,2)+pow(horizontal_distance,2))

    def manhattanDistance(self,end_position):
        vertical_distance = abs(end_position[1]-self.state[1])
        horizontal_distance = abs(end_position[0]-self.state[0])
        return vertical_distance+horizontal_distance
    def heuristics(self,distance,end_position):
        if distance == "euclidean":
            return self.euclideanDistance(end_position)
        elif distance == "manhattan":
            return self.manhattanDistance(end_position)
    def checkEnd(self):
        if self.x == end_position[0] and self.y == end_position[1]:
            #print ('This is the end')
            return True
        else:
            return False
    def validMove(self,moves):
        if moves == "U":
         return self.elevate_value(self.x,self.y-1) != "X"
        elif moves == "D":
         return self.elevate_value(self.x,self.y+1) != "X"
        elif moves == "L":
         return self.elevate_value(self.x-1,self.y) != "X"
        elif moves == "R":
         return self.elevate_value(self.x+1,self.y) != "X"
    
    def move(self):
        if self.validMove("U"):
            self.up = Nodes(self,[self.x,self.y-1],end_position,size_of_map,initial_map)
        else:
            #print(f'{self.position()}cannot go up')
            self.up = None
        
        if self.validMove("D"):
            self.down = Nodes(self,[self.x,self.y+1],end_position,size_of_map,initial_map)
        else:
            #print(f'{self.position()}cannot go down')
            self.down = None
        
        if self.validMove("L"):
            self.left = Nodes(self,[self.x-1,self.y],end_position,size_of_map,initial_map)
        else:
            #print(f'{self.position()}cannot go left')
            self.left = None
        
        if self.validMove("R"):
            self.right = Nodes(self,[self.x+1,self.y],end_position,size_of_map,initial_map)
        else:
            #print(f'{self.position()}cannot go left')
            self.right = None

    
    def finalPath(self):
        path_list = []
        path_list.append(self.state)
        node = self
        while node.parent.state[0] != start_position[0] or node.parent.state[1] != start_position[1]:
            #print(node.parent.state)
            path_list.append(node.parent.state)
            node = node.parent
        path_list.append(node.parent.state)
        return path_list

    def printFinalMap(self,path_list):
        #with open("FinalMap.txt","w") as f:
            
        for x in range(1, size_of_map[0] + 1):
            for y in range(1, size_of_map[1] + 1):
                if [x,y] in path_list:
                    print("*",end=" ") 
                elif y == size_of_map[1]:
                    print(initial_map[x][y])
                else:
                    print(initial_map[x][y],end=" ")
        # for y in range(1, size_of_map[1] + 1):
        #     for x in range(1, size_of_map[0] + 1):
        #         if [y,x] in path_list:
        #             print("*",end=" ") 
        #         else:
        #             print(initial_map[x][y],end=" ")
        #     print("\n")
            
        #with open("FinalMap.txt","r") as f:
        ##    file_contents = f.read()
        #    print(file_contents)
    def pathcost(self, neighbour):
        if neighbour.elevate_value(neighbour.x,neighbour.y) - self.elevate_value(self.x,self.y) > 0:
            return 1 + neighbour.elevate_value(neighbour.x,neighbour.y) - self.elevate_value(self.x,self.y)
        else:
            return 1

    def updateCosthistory(self,cost):
        self.cost_history = cost     

    def bfsearch(self):
        try:
            path_queue = Queue()
            visited_list = []
            count = 0
            path_queue.put(self)
            node = path_queue.get()
            visited_list.append(node.state)
            #print(f'This is visited set{visited_list}')
            if self != None:
                while node.checkEnd() == False:
                #while count < 100:
                    
                    node.move()
                    test_counter = 0
                    if node.left != None:
                        if node.left.state not in visited_list:
                            for elem in list(path_queue.queue):
                                if node.left.state == elem.state:
                                    test_counter = 1
                            if test_counter == 0:
                                path_queue.put(node.left)
                        else:
                            #print(f'Visited {node.left.state}')
                            pass
                    test_counter = 0
                    if node.right != None:
                        if node.right.state not in visited_list:
                            for elem in list(path_queue.queue):
                                if node.right.state == elem.state:
                                    test_counter = 1
                            if test_counter == 0:
                                path_queue.put(node.right)
                        else:
                            #print(f'Visited {node.right.state}')
                            pass
                    test_counter = 0
                    if node.up != None:
                        if node.up.state not in visited_list:
                            for elem in list(path_queue.queue):
                                if node.up.state == elem.state:
                                    test_counter = 1
                            if test_counter == 0:
                                path_queue.put(node.up)
                        else:
                            #print(f'Visited {node.up.state}')
                            pass
                    test_counter = 0
                    if node.down != None:
                        if node.down.state not in visited_list:
                            for elem in list(path_queue.queue):
                                if node.down.state == elem.state:
                                    test_counter = 1
                            if test_counter == 0:
                                path_queue.put(node.down)
                        else:
                            #print(f'Visited {node.down.state}')
                            pass

                    if path_queue.empty():
                        return None
                    else:
                        node = path_queue.get()
                    visited_list.append(node.state)                
                    count +=1
                    #print (f'layer {count}') 
                    #print(f'This is visited set{visited_list}')
                    #print(node.position())
                return node
            else:
                return None        
                
        except Exception as inst:
            #print(inst)
            return None
            

    def uniformCostSearch(self):
        try:
            path_queue = []
            visited_list = []
            count = float(0)
            base = float(10000000000)
            heapq.heappush(path_queue, (1, self))
            temp, node = heapq.heappop(path_queue)
            visited_list.append(node.state)
            #print(f'This is visited set{visited_list}')
            if self != None:
                while node.checkEnd() == False:
                #while count < 100:
                    node.move()

                    if node.left != None:
                        if node.left.state not in visited_list:
                            count +=1
                            heapq.heappush(path_queue, (node.pathcost(node.left)+count/base, node.left))
                        else:
                            #print(f'Visited {node.left.state}')
                            pass
                    
                    if node.right != None:
                        if node.right.state not in visited_list:
                            count +=1
                            heapq.heappush(path_queue, (node.pathcost(node.right)+count/base, node.right))
                        else:
                            #print(f'Visited {node.right.state}')
                            pass

                    if node.up != None:
                        if node.up.state not in visited_list:
                            count +=1
                            heapq.heappush(path_queue, (node.pathcost(node.up)+count/base, node.up))
                            
                        else:
                            #print(f'Visited {node.up.state}')
                            pass
                        
                    if node.down != None:
                        if node.down.state not in visited_list:
                            count +=1
                            heapq.heappush(path_queue, (node.pathcost(node.down)+count/base, node.down))
                            
                        else:
                            #print(f'Visited {node.down.state}')
                            pass

                    
                        

                    temp, node = heapq.heappop(path_queue)
                    visited_list.append(node.state)                
                    
                    #print (f'layer {count}') 
                    #print(f'This is visited set{visited_list}')
                return node
        except:
            return None
    def aStarSearch(self,distance):
        try:

            path_queue = []
            visited_list = []
            count = float(0)
            base = float(10000000000)
            heapq.heappush(path_queue, (1, self))
            temp, node = heapq.heappop(path_queue)
            visited_list.append(node.state)
            #print(f'This is visited set{visited_list}')
            if self != None:
                while node.checkEnd() == False:
                #while count < 100:
                    node.move()

                    if node.left != None:
                        if node.left.state not in visited_list:
                            count +=1
                            node.left.updateCosthistory(node.cost_history + node.pathcost(node.left))
                            heapq.heappush(path_queue, (node.left.cost_history + node.left.heuristics(distance,end_position)+count/base, node.left))
                        else:
                        #print(f'Visited {node.left.state}')
                            pass
                        
                    if node.right != None:
                        if node.right.state not in visited_list:
                            count +=1
                            node.right.updateCosthistory(node.cost_history + node.pathcost(node.right))
                            heapq.heappush(path_queue, (node.right.cost_history + node.right.heuristics(distance,end_position)+count/base, node.right))
                        else:
                            #print(f'Visited {node.right.state}')
                            pass

                    if node.up != None:
                        if node.up.state not in visited_list:
                            count +=1
                            node.up.updateCosthistory(node.cost_history + node.pathcost(node.up))
                            heapq.heappush(path_queue, (node.up.cost_history + node.up.heuristics(distance,end_position) + count/base, node.up))
                            
                        else:
                            #print(f'Visited {node.up.state}')
                            pass
                        
                    if node.down != None:
                        if node.down.state not in visited_list:
                            count +=1
                            node.down.updateCosthistory(node.cost_history + node.pathcost(node.down))
                            heapq.heappush(path_queue, (node.down.cost_history+ node.down.heuristics(distance,end_position)+count/base, node.down))
                            
                        else:
                            #print(f'Visited {node.down.state}')
                            pass
                    
                            

                    temp, node = heapq.heappop(path_queue)
                    visited_list.append(node.state)                
                    #if count >100000:
                    #   return None
                    #print (f'layer {count}') 
                    #print(f'This is visited set{visited_list}')
                return node
        except:
            return None 

if __name__ == "__main__":

    map_txt = sys.argv[1]
    algorithm = sys.argv[2]
    try:
        heuristic = sys.argv[3]
    except:
        pass
    
    f = open(map_txt)
    readMap = csv.reader(f)

    size_of_map_text = next(readMap)
    start_position_text = next(readMap)
    end_position_text = next(readMap)

    state_map_list = []
    for row in readMap:
        state_map_list.append(row[0].split(" "))

    state_map = state_map_list

    size_of_map = list(map(int,size_of_map_text[0].split(" ")))

    start_position = list(map(int,start_position_text[0].split(" ")))

    end_position = list(map(int,end_position_text[0].split(" ")))

    # print(size_of_map)
    # print(start_position)
    # print(end_position)
    # print(state_map_list[1])

    temp_map = []
    for iy in range(size_of_map[0]+2):
        temp_row = []
        if iy == 0:
            for ix in range(size_of_map[1]+2):
                    temp_row.append("X")
        elif iy == size_of_map[0]+1:
            for ix in range(size_of_map[1]+2):
                    temp_row.append("X")
        else:
            temp_row.append("X")
            for ix in range(size_of_map[1]):
                temp_row.append(state_map_list[iy-1][ix])
            temp_row.append("X")
        temp_map.append(temp_row)


    initial_map = temp_map

    # for row in initial_map:
    #     for i in row:
    #         print(i,end = ' ')
    #     print("\n")


    node = Nodes(None,start_position,end_position,size_of_map,initial_map)
    node.move()
    
    if algorithm == "bfs":
        end_node = node.bfsearch()
    elif algorithm == "ucs":
        end_node = node.uniformCostSearch()
    elif algorithm == "astar":
        if heuristic == "euclidean":
            end_node = node.aStarSearch("euclidean")
        elif heuristic == "manhattan":
            end_node = node.aStarSearch("manhattan")
    if end_node == None:
        print("null")
    else:
        path_list = end_node.finalPath()
        #print(path_list)
        end_node.printFinalMap(path_list)
