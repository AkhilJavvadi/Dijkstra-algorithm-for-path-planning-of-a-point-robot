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

        cv.destroyAllWindows()