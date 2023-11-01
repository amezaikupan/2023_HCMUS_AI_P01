from A_star import a_star_algorithm
from helper import get_map
# from Level3 import Init_Pacman_view

map , size, pos= get_map("../test/lv3_map1.txt")


# path = a_star_algorithm(map, pos)
# print (path)

# view = Init_Pacman_view(map, pos)

# for row in map:
#     print (row)
# for item in view:
#     print (item)

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return list(reversed(path))

def updateMazePacman(maze, mazePacman, pacmanPos, mazeFood):
    rows = len(maze)
    cols = len(maze[0])

    for i in range(rows):
        for j in range(cols):
            if abs(i - pacmanPos[0]) + abs(j - pacmanPos[1]) <= 3:
                mazePacman[i][j] = maze[i][j]

    for i in range(rows):
        for j in range(cols):
            if mazePacman[i][j] != 4 and mazeFood[i][j] == 2 and mazePacman[i][j] != 0:
                mazePacman[i][j] = mazeFood[i][j]
    return mazePacman

def initfoodmaze(maze):
    mazeFood = [[maze[row][col] for col in range(len(maze[0]))] for row in range(len(maze))]
    return mazeFood

def initMazePacmanView(maze):
    rows = len(maze)
    cols = len(maze[0])

    # Khởi tạo mảng  2 chiều mới với kích thước và giá trị như yêu cầu
    mazePacman = [[4 for _ in range(cols)] for _ in range(rows)]
    
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 1:
                mazePacman[i][j] = 1
    return mazePacman

maze, size, start = get_map("../test/lv3_map1.txt")
mazeFood = initfoodmaze(maze)

mazePacman = initMazePacmanView(maze)
pacmanPos = tuple(start)
mazePacman = updateMazePacman(maze, mazePacman, pacmanPos, mazeFood)

for line in mazePacman:
        print (line)
x = pacmanPos[0]
y = pacmanPos[1]
for i in range(10):
    y +=1
    newpos = (x,y)
    mazePacman = updateMazePacman(maze, mazePacman, newpos, mazeFood)
    print ("+++++++++++++++++++++++++++++++++++++++")
    for line in mazePacman:
        print (line)
