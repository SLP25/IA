import graph.graph_parser as gp
import time
import os

def show_race(graph, matrix, path):
    (rows, cols) = gp.get_matrix_dimensions(matrix)
    node = path.pop(0)
    car = (node.x, node.y)
    cost = 0
    
    __show_cost__(cost)
    __show_board__(matrix, rows, cols, car)

    while len(path) != 0:
        time.sleep(0.25)
        
        next = path.pop(0)
        
        for (n,c) in graph.adjList[node]:
            if next == n:
                add = c
                break

        if add == 25:
            car_char = '▒'
        else:
            car_char = '█'
        
        cost += add
        node = next
        car = (node.x, node.y)  
        
        os.system("clear")
        __show_cost__(cost)
        __show_board__(matrix, rows, cols, car, car_char)
        
        
def __show_cost__(cost):
    print(f"Current cost: {cost}           ")

def __show_board__(matrix, rows, cols, car, car_char = '█'):
    for y in range(0, rows):
        for x in range(0, cols):
            if (x,y)==car:
                print(car_char, end='')
            else:
                print(matrix[y][x], end='')
        print()