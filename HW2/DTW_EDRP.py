import numpy as np
import math
#return DTW distance

#use euclidean distance
def distance_matrix_DTW(x, y):
    distance = np.zeros((len(y), len(x)))
    for i in range(len(y)):
        for j in range(len(x)):
            distance[i,j] = math.sqrt((x[j]-y[i])**2)
    return distance

def distance_matrix_EDRP(x, y):
    distance = np.zeros((len(y), len(x)))
    for i in range(len(y)):
        for j in range(len(x)):
            if i > (len(x)-1):
                distance[i,j] = x[j]
            elif j > (len(y)-1):
                distance[i,j] = y[i]
            else:
                distance[i,j] = math.sqrt((x[j]-y[i])**2)
    return distance

#minimum distance to reach a point when starting from [0,0]
def cost_matrix(x, y, distances):
    accumulated_cost = np.zeros((len(y), len(x)))
    accumulated_cost[0,0] = distances[0,0]
    #fill distances to right
    for i in range(1, len(x)):
        accumulated_cost[0,i] = distances[0,i] + accumulated_cost[0, i-1]    
    #fill distances in 1st column
    for i in range(1, len(y)):
        accumulated_cost[i,0] = distances[i, 0] + accumulated_cost[i-1, 0]
    #all other elements
    for i in range(1, len(y)):
        for j in range(1, len(x)):
            accumulated_cost[i, j] = min(accumulated_cost[i-1, j-1], accumulated_cost[i-1, j], accumulated_cost[i, j-1]) + distances[i, j]
    return accumulated_cost

def calculate_path(x, y, distance):
    distances = distance(x, y)
    accumulated_cost = cost_matrix(x, y, distances)
    cost = 0
    #backtracking to find minimum path
    path = [[len(x)-1, len(y)-1]]
    i = len(y)-1
    j = len(x)-1
    while i>0 and j>0:
        if i==0:
            j = j - 1
        elif j==0:
            i = i - 1
        else:
            if accumulated_cost[i-1, j] == min(accumulated_cost[i-1, j-1], accumulated_cost[i-1, j], accumulated_cost[i, j-1]):
                i = i - 1
            elif accumulated_cost[i, j-1] == min(accumulated_cost[i-1, j-1], accumulated_cost[i-1, j], accumulated_cost[i, j-1]):
                j = j-1
            else:
                i = i - 1
                j= j- 1
        path.append([j, i])
    path.append([0,0])
    for [y, x] in path:
        cost = cost +distances[x, y]
    return (path, cost)
