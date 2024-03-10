import cv2 as cv
import numpy as np
import time 
from queue import PriorityQueue

#creating the clearance and obstacle colour
clearance = 5 
obstracle = (0,0,255)

#defining Linear equation for obstacles
def linear_equation(i,j,x1,y1,x2,y2,clearance):
    if x2 - x1 == 0:
        # handle case where the denominator is zero
        if i == x1:
            return j - y1
        else:
            return float('inf')
    else:
        return ((y2 - y1) / (x2 - x1 + clearance)) * (i - x1 - clearance/2) + y1 - j

#Generating map
def Map_Generator(height, width):

    map = np.zeros((height, width, 3))
    for i in range(map.shape[1]):
        for j in range(map.shape[0]):
        #rectangle obstacle1
            if(i>=100 and i<=175 and j>=0 and j<=400):
                map[j][i] = obstracle
        #rectangle obstacle 2
            if(i>=275 and i<=350 and j>=100 and j<=500):
                map[j][i] = obstracle
        #hexagon obstacle
            if(linear_equation(i,j,*(650,100),*(780,175),clearance)<=0 and i<780 and linear_equation(i,j,*(780,325),*(650,400),clearance)>=0
           and linear_equation(i,j,*(650,400),*(520,325),clearance)>=0 and i>520 and linear_equation(i,j,*(520,175),*(650,100),clearance)<=0):
                map[j][i] = obstracle
        #rectangle obstacle3
            if(i>=900 and i<=1020 and j>=50 and j<=125):
                map[j][i] = obstracle
        #rectangle obstacle4
            if(i>=900 and i<=1020 and j>=375 and j<=450):
                map[j][i] = obstracle
        #rectangle obstacle1
            if(i>=1020 and i<=1100 and j>=50 and j<=450):
                map[j][i] = obstracle
    return map

#defining the obstacles
def isObstacle(map, x, y):
 
    if (map[x][y][2] < obstracle[2]):
        return False
    else:
        return True
    
# Checking for applicable inputs 
def checkInputFeasibility(x_start, y_start, x_goal, y_goal, map):
 
    input_flag = True

    if isObstacle(map, y_start, x_start):
        print("!! Start Position is in an Obstacle/Wall, try again!")
        input_flag = False
    if isObstacle(map, y_goal, x_goal):
        print("!! Goal Position is in an Obstacle/Wall!, try again")
        input_flag = False
    
    return input_flag

# Function to Move Top 
def actionMoveTop(CurrentNode,map):

    NextNode = list(CurrentNode)
    if(NextNode[1]-1 > 0) and (not isObstacle(map, NextNode[1]-1, NextNode[0])):
        Status = True
        NextNode[1] = NextNode[1] - 1 
    else:
        Status = False   

    return (Status, NextNode)

# Function to Move diagonally top right of cost 1.4
def actionMoveTopRight(CurrentNode,map):

    NextNode = list(CurrentNode)
    
    if(NextNode[1]-1 > 0) and (NextNode[0]+1 <map.shape[1]) and (not isObstacle(map, NextNode[1]-1, NextNode[0])):
        Status = True
        NextNode[0] = NextNode[0] + 1 
        NextNode[1] = NextNode[1] - 1
    else:
        Status = False   

    return (Status, NextNode)

# Function to Move Right diagonally
def actionMoveRight(CurrentNode,map):
    
    NextNode = list(CurrentNode)
    if(NextNode[0]+1 <map.shape[1]) and (not isObstacle(map, NextNode[1], NextNode[0]+1)):
        Status = True
        NextNode[0] = NextNode[0] + 1 
    else:
        Status = False   

    return (Status, NextNode)

# Function to Move Bottom Right
def actionMoveBottomRight(CurrentNode,map):
    
    NextNode = list(CurrentNode)
    if(NextNode[1]+1 < map.shape[0]) and (NextNode[0]+1 <map.shape[1]) and (not isObstacle(map, NextNode[1]+1, NextNode[0]+1)):
        Status = True
        NextNode[0] = NextNode[0] + 1 
        NextNode[1] = NextNode[1] + 1
    else:
        Status = False   

    return (Status, NextNode)

# Function to Move Bottom
def actionMoveBottom(CurrentNode,map):
    
    NextNode = list(CurrentNode)
    if(NextNode[1]+1 < map.shape[0]) and (not isObstacle(map, NextNode[1]+1, NextNode[0])):
        Status = True 
        NextNode[1] = NextNode[1] + 1
    else:
        Status = False   

    return (Status, NextNode)

# Function to Move Bottom Left(Diagonally)
def actionMoveBottomLeft(CurrentNode,map):
    
    NextNode = list(CurrentNode)
    if(NextNode[1]+1 < map.shape[0]) and (NextNode[0]-1 >0) and (not isObstacle(map, NextNode[1]+1, NextNode[0]-1)):
        Status = True 
        NextNode[0] = NextNode[0] - 1
        NextNode[1] = NextNode[1] + 1
    else:
        Status = False   

    return (Status, NextNode)

# Function to Move Left
def actionMoveLeft(CurrentNode,map):
    
    NextNode = list(CurrentNode)
    if(NextNode[0]-1 > 0) and (not isObstacle(map, NextNode[1], NextNode[0]-1)):  
        Status = True 
        NextNode[0] = NextNode[0] - 1
    else:
        Status = False   

    return (Status, NextNode)

# Function to Move Top Left (Diagonally)
def actionMoveTopLeft(CurrentNode,map):
    
    NextNode = list(CurrentNode)
    if(NextNode[1]-1 > 0) and (NextNode[0]-1 > 0) and (not isObstacle(map, NextNode[1]-1, NextNode[0]-1)):
        Status = True 
        NextNode[0] = NextNode[0] - 1
        NextNode[1] = NextNode[1] - 1
    else:
        Status = False   

    return (Status, NextNode)

def Dijkstra_algo(startNode, goalNode, map):
    
    closed_list = {}    
    opened_list = PriorityQueue()    

    opened_list.put((0, startNode, startNode))
    visited = set()  # Track visited nodes to avoid duplicates
    
    start_time = time.time()
    while not opened_list.empty():
        
        cost_to_come, present_node, parent_node = opened_list.get()
        present_node = tuple(present_node)  # Convert list to tuple
        visited.add(present_node)  # Mark present node as visited
        
        closed_list[(present_node[0], present_node[1])] = parent_node
        
        if isGoalNode(present_node, goalNode):
            print("\n Goal reached!")
            end_time = time.time()
            print("\nTime: "+str(round((end_time-start_time), 4)) + " [secs]")
            back_Tracking_Algo(goalNode, startNode, closed_list, map)
            return True

        for action in [actionMoveTop, actionMoveTopRight, actionMoveRight,
               actionMoveBottomRight, actionMoveBottom, actionMoveBottomLeft,
               actionMoveLeft, actionMoveTopLeft]:
            flag, child_node = action(present_node, map)
            child_node_tuple = tuple(child_node)  # Convert list to tuple
            if flag is True and child_node_tuple not in visited:
                if not isGoalNode(child_node_tuple, goalNode):
                    cost = cost_to_come + (1 if action in [actionMoveTop, actionMoveRight,
                                                            actionMoveBottom, actionMoveLeft] else 1.4)
                    child_node = list(child_node_tuple)  # Convert tuple back to list for further processing
                    opened_list.put((cost, child_node, present_node))
                    visited.add(child_node_tuple)  # Add tuple to visited set
                else:
                    print("\nGoal reached!")
                    end_time = time.time()
                    print("\nTime: "+str(round((end_time-start_time), 4)) + " [secs]")
                    closed_list[child_node_tuple] = present_node
                    back_Tracking_Algo(goalNode, startNode, closed_list, map)
                    return True



    print("\n No path found between the start and goal explored_nodes") 
    return False

# Calling the map generating functions 
if __name__ == '__main__':
# display map with original obstracles  
    map = Map_Generator(500, 1200)                 
    print('Enter the start position:')
    x_start = int(input("Enter your value of X-Axis: "))
    y_start = int(input("Enter your value of Y-Axis: "))
    print('Enter the goal position:')
    x_goal = int(input("Enter your value of X-Axis: "))
    y_goal = int(input("Enter your value of Y-Axis: "))
    if (checkInputFeasibility(x_start, y_start, x_goal, y_goal, map)):
        startNode = [x_start, y_start]
        goalNode = [x_goal, y_goal]

        res = Dijkstra_algo(startNode, goalNode, map)

        cv.destroyAllWindows()