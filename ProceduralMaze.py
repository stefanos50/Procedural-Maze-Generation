import random
import matplotlib.pyplot as plt
import numpy as np


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    # Search function

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def apply_union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    #  Applying Kruskal algorithm
    def kruskal_algo(self):
        result = []
        i, e = 0, 0
        self.graph = sorted(self.graph, key=lambda item: item[2])
        parent = []
        rank = []
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
        while e < self.V - 1:
            u, v, w = self.graph[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.apply_union(parent, rank, x, y)
        return result

maze_x = int(input("Enter maze size x: "))
maze_y = int(input("Enter maze size y: "))
max_random_weight = int(input("Enter max random weight: "))
g = Graph(maze_x * maze_y)

#Create the graph connection

#Connect each node with the nearest right node
step = maze_x
for i in range(maze_y):
    for j in range(maze_x):
        if((i*step)+j+1 >= maze_x+((i*step))):
            break
        g.add_edge((i*step)+j, (i*step)+j+1, random.randint(1, max_random_weight))

#Connect each node with the bottom nearest node
c_x = 0
c_y = maze_x
for i in range(maze_x):
    c_x = i
    c_y = i+maze_x
    for j in range(maze_y-1):
        g.add_edge(c_x, c_y, random.randint(1, max_random_weight))
        c_x += maze_x
        c_y += maze_x

#Get the kruskal final connections
res = g.kruskal_algo()
res_tuples = []
for u, v, weight in res:
    print("%d - %d: %d" % (u, v, weight))
    res_tuples.append((u,v))

#Double the maze array for the obstacles
maze_array = np.zeros((maze_y*2-1,maze_x*2-1))

#Find and update the maze array for the horizontal connections
cell_x = 0
cell_y = 1
for i in range(0,maze_y*2-1):
    if (i % 2 == 1):
        continue
    for j in range(0,maze_x*2-1,2):
        if (cell_x,cell_y) in res_tuples and abs(cell_x-cell_y) == 1:
            maze_array[i][j] = 1
            maze_array[i][j+1] = 1
            maze_array[i][j+2] = 1
        cell_x += 1
        cell_y +=1

#Find and update the maze array for the vertical connections
last = 0
cell_x = 0
cell_y = maze_x
for i in range(maze_x*2-1):
    if (i % 2 == 1):
        continue
    for j in range(0,maze_y*2-1,2):
        if (cell_x,cell_y) in res_tuples and abs(cell_x-cell_y) == maze_x:
            maze_array[j][i] = 1
            maze_array[j+1][i] = 1
            maze_array[j+2][i] = 1
        cell_x = cell_y
        cell_y += maze_x
    last += 1
    cell_x = last
    cell_y = last + maze_x

#Add walls to all sides
maze_array = np.pad(maze_array, [(0, 1), (0, 1)], mode='constant')
maze_array = np.pad(maze_array, [(1, 0), (1, 0)], mode='constant')
print(maze_array)

#plot the final maze from the array representation
plt.imshow(maze_array)
plt.show()