from __future__ import print_function
import csv
import math
import Queue
import heapq
import sys
import random 

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
        self.end = end_position
        self.map = initial_map
        
    def position(self):
        #print(f'[{self.x},{self.y}]')
        return [self.x, self.y]
    
    def checkEnd(self):
        if self.x == self.end[0] and self.y == self.end[1]:
            #print ('This is the end')
            #print(self.end)
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
            self.up = Nodes(self,[self.x,self.y-1],self.end,size_of_map,self.map)
        else:
            #print(f'{self.position()}cannot go up')
            self.up = None
        
        if self.validMove("D"):
            self.down = Nodes(self,[self.x,self.y+1],self.end,size_of_map,self.map)
        else:
            #print(f'{self.position()}cannot go down')
            self.down = None
        
        if self.validMove("L"):
            self.left = Nodes(self,[self.x-1,self.y],self.end,size_of_map,self.map)
        else:
            #print(f'{self.position()}cannot go left')
            self.left = None
        
        if self.validMove("R"):
            self.right = Nodes(self,[self.x+1,self.y],self.end,size_of_map,self.map)
        else:
            #print(f'{self.position()}cannot go left')
            self.right = None
    

    def elevate_value(self,x,y,alter_map = None):
        #print(x)
        #print(y)
        #print(initial_map)
        if alter_map == None:
            elevate_value = self.map[x][y]
        else:
            elevate_value = alter_map[x][y]
        #print(f'x:{x} y:{y} elevate_value:{elevate_value}')
        if elevate_value !="X":
            if  elevate_value !="*":
                return int(elevate_value)
            else: 
                return elevate_value
        else: 
                return elevate_value

    def pathcost(self, neighbour,alter_map = None):
        if alter_map == None:

            if neighbour.elevate_value(neighbour.x,neighbour.y) - self.elevate_value(self.x,self.y) > 0:
                return 1 + neighbour.elevate_value(neighbour.x,neighbour.y) - self.elevate_value(self.x,self.y)
            else:
                return 1
        else:
            if neighbour.elevate_value(neighbour.x,neighbour.y,alter_map) - self.elevate_value(self.x,self.y,alter_map) > 0:
                return 1 + neighbour.elevate_value(neighbour.x,neighbour.y,alter_map) - self.elevate_value(self.x,self.y,alter_map)
            else:
                return 1

    def pospathcost(self, pos, neighbour,alter_map = None):
        if alter_map == None:
            if self.elevate_value(neighbour[0],neighbour[1]) - self.elevate_value(pos[0],pos[1]) > 0:
                return 1 + self.elevate_value(neighbour[0],neighbour[1]) - self.elevate_value(pos[0],pos[1])
            else:
                return 1
        else:
            if self.elevate_value(neighbour[0],neighbour[1],alter_map) - self.elevate_value(pos[0],pos[1],alter_map) > 0:
                return 1 + self.elevate_value(neighbour[0],neighbour[1],alter_map) - self.elevate_value(pos[0],pos[1],alter_map)
            else:
                return 1

    def total_pathcost(self,pathlist,alter_map = None):
        if alter_map == None:
            total_cost = 0
            for pos in range(len(pathlist)-1):
                total_cost += self.pospathcost(pathlist[pos+1],pathlist[pos])
            return total_cost
        else:
            total_cost = 0
            for pos in range(len(pathlist)-1):
                total_cost += self.pospathcost(pathlist[pos+1],pathlist[pos],alter_map)
            return total_cost

    
    def updateCosthistory(self,cost):
        self.cost_history = cost    

    def finalPath(self,start):
        path_list = []
        path_list.append(self.state)
        node = self
        while node.parent.state[0] != start[0] or node.parent.state[1] != start[1]:
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
                    if y == size_of_map[1]:
                        print("*")  
                    else:
                        print("*",end=" ") 
                elif y == size_of_map[1]:
                    print(self.map[x][y])
                else:
                    print(self.map[x][y],end=" ")
            

    def bfsearch(self,):
        try:
            path_queue = Queue.Queue()
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

                    if node.left != None:
                        if node.left.state not in visited_list:
                            path_queue.put(node.left)
                        else:
                            #print(f'Visited {node.left.state}')
                            pass
                    
                    if node.right != None:
                        if node.right.state not in visited_list:
                            path_queue.put(node.right)
                        else:
                            #print(f'Visited {node.right.state}')
                            pass

                    if node.up != None:
                        if node.up.state not in visited_list:
                            path_queue.put(node.up)
                        else:
                            #print(f'Visited {node.up.state}')
                            pass
                        
                    if node.down != None:
                        if node.down.state not in visited_list:
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
                
        except:
            return None
    
    def randomised_bfsearch(self):
        try:
            path_queue = Queue.Queue()
            visited_list = []
            count = 0
            path_queue.put(self)
            node = path_queue.get()
            visited_list.append(node.state)
            expand_order = ["U","D","L","R"]
            #print(f'This is visited set{visited_list}')
            if self != None:
                while node.checkEnd() == False:
                    node.move()
                    random.shuffle(expand_order)
                    #print(expand_order)
                    for direction in expand_order:
                        if direction == "U":
                            if node.left != None:
                                if node.left.state not in visited_list:
                                    path_queue.put(node.left)
                                else:
                                    #print(f'Visited {node.left.state}')
                                    pass
                        if direction == "D":
                            if node.right != None:
                                if node.right.state not in visited_list:
                                    path_queue.put(node.right)
                                else:
                                    #print(f'Visited {node.right.state}')
                                    pass
                        if direction == "L":
                            if node.up != None:
                                if node.up.state not in visited_list:
                                    path_queue.put(node.up)
                                else:
                                    #print(f'Visited {node.up.state}')
                                    pass
                        if direction == "R":
                            if node.down != None:
                                if node.down.state not in visited_list:
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
            #print(node.position())
            return None
    
    def searchforpath(self):
        try:
            path_queue = Queue.Queue()
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

                    if node.left != None:
                        if node.left.elevate_value(node.left.x,node.left.y) == "*":
                            path_queue.put(node.left)
                        else:
                            #print(f'Visited {node.left.state}')
                            pass
                    
                    if node.right != None:
                        if node.right.elevate_value(node.right.x,node.right.y) == "*":
                            path_queue.put(node.right)
                        else:
                            #print(f'Visited {node.right.state}')
                            pass

                    if node.up != None:
                        if node.up.elevate_value(node.up.x,node.up.y) == "*":
                            path_queue.put(node.up)
                        else:
                            #print(f'Visited {node.up.state}')
                            pass
                        
                    if node.down != None:
                        if node.down.elevate_value(node.down.x,node.down.y) == "*":
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
        
if __name__ == "__main__":

    map_txt = sys.argv[1]
    init_path = sys.argv[2]
    init_temperature_txt = sys.argv[3]
    final_temperature_txt = sys.argv[4]
    alpha_txt = sys.argv[5]
    segment_length_txt = sys.argv[6]
    init_temperature = float(init_temperature_txt)
    final_temperature = float(final_temperature_txt)
    alpha = float(alpha_txt)
    segment_length = int(segment_length_txt)

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

    initial_start_map = temp_map
    f.close()
    f2 = open(init_path)
    readMap = csv.reader(f2)

    init_path_map_list = []
    for row in readMap:
	#print(row)
	#print(row[0])
	#print(row[0].split(" "))
        init_path_map_list.append(row[0].split(" "))

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
                temp_row.append(init_path_map_list[iy-1][ix])
            temp_row.append("X")
        temp_map.append(temp_row)

    init_path_map = temp_map
    #print(init_path_map)
    # for row in initial_map:
    #     for i in row:
    #         print(i,end = ' ')
    #     print("\n")


    #node = Nodes(None,start_position,end_position,size_of_map,initial_map)
    
    #end_node = node.bfsearch()
    
    #if end_node == None:
    #     print("null")
    # else:
    #     path_list = end_node.finalPath(start_position)
    #     print(path_list)
    #     end_node.printFinalMap(path_list)

    node = Nodes(None,start_position,end_position,size_of_map,init_path_map)
    end_node = node.searchforpath()

    if end_node == None:
         print("null")
    else:
        path_list = end_node.finalPath(start_position)
        #print(path_list)
        #end_node.printFinalMap(path_list)
    #print(" ")
    g_original_pathcost = node.total_pathcost(path_list,initial_start_map)
    #print(g_original_pathcost)

    T = float(init_temperature)
    #print(f'this is T:{T}')
    final_path_list = path_list
    T_list = []
    cost_list = []
    while T > final_temperature:
        #print(f'this is T:{T} f_temp:{final_temperature}')

        rand_position = random.choice(final_path_list[1:])
        #print(rand_position)
        if path_list.index(rand_position)-segment_length < 0:
            next_position = path_list[0]
        else:
            next_position = path_list[path_list.index(rand_position)-segment_length]
        #print(next_position)
        new_node = Nodes(None,rand_position,next_position,size_of_map,initial_start_map)
        
        temp_end_node = new_node.randomised_bfsearch()
        temp_finalpath_list = temp_end_node.finalPath(rand_position)
        
        if path_list.index(rand_position)-segment_length < 0:
            length = path_list.index(rand_position) - path_list.index(end_position)
            start_index = 0
        else:
            length = segment_length
            start_index = path_list.index(rand_position)-segment_length
        temp_path_list = []
        
        temp_path_list = path_list

        for i in range(length):
            temp_path_list.remove(temp_path_list[start_index])
            #print(temp_path_list)
        for i in range(len(temp_finalpath_list)-1):
            temp_path_list.insert(start_index+i,temp_finalpath_list[i])

        g_temp_pathcost = new_node.total_pathcost(temp_path_list)
        g_different = g_original_pathcost - g_temp_pathcost

        if g_different > 0:
            final_path_list = temp_path_list
            cost_list.append(g_temp_pathcost)
            g_original_pathcost = g_temp_pathcost
        else:
            if random.random() < math.exp(float(g_different)/T)/float(100):
                #print(f'this is e:{math.exp(float(g_different)/T)/float(100)}')
                final_path_list = temp_path_list
                cost_list.append(g_temp_pathcost)
                g_original_pathcost = g_temp_pathcost
            else:
                cost_list.append(g_original_pathcost)
        T_list.append(T)
        #T = final_temperature
        T = alpha * T
    # print(f'this is final path list')
    # print(temp_finalpath_list)
    # print(f'this is temp path list')
    # print(temp_path_list)
    #print(f'this is total_pathcost')
    #print(new_node.total_pathcost(temp_path_list))
    #print(f'this is final pathcost')
    #print(new_node.total_pathcost(final_path_list))

    new_node.printFinalMap(final_path_list)
    #print(T_list)
    for i , item in enumerate(cost_list):
        print('T=',T_list[i], 'cost =',item)
            

