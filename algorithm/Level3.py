from algorithm.A_star import find_heuristic,get_neighbors, a_star_algorithm
from graphic.util import readMap
import random
import math

#Find all the position in the map for all types of object
def FindObject(map, type):
    pos_list = []
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == type:
                pos_list.append((i,j))
    return pos_list

#Function to handle move of monsters randomly one step
def MonsterMove(map, monsters):
    MonstersPos = []
    for monster in monsters:
        x = monster[0]
        y = monster[1]
        #Find the position of neighbor in left, down, up, right side
        movable_pos = [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]
        valid_pos = []
        for pos in movable_pos:
            x = pos[0]
            y = pos[1]
            #Check the pos is in the map, and not blocked by wall
            if( 0 <= x < len(map) and 0 <= y < len(map[0])  and map[x][y] != 1 and map[x][y] != 2 ):
                valid_pos.append((x,y)) # If true, it is a valid position.
            
        move = random.choice(valid_pos) #Choice the next move randomly
       
       #Update the map
        map[move[0]][move[1]] = 3
        map[monster[0]][monster[1]] = 0

        MonstersPos.append(move)

    return MonstersPos,map

#Because in level 3, pacman has a limited visible range, so I change all the value of map into another value (specifically 4)
def Init_Pacman_view(map):
    rows = len(map)
    cols = len(map[0])

    Pacman_view = [[4 for _ in range(cols)] for _ in range(rows)]
    
    for i in range(rows):
        for j in range(cols):
            if map[i][j] == 1:
                Pacman_view[i][j] = 1
    
    return Pacman_view

#Set the visible range of Pacman 
#Update the current view of Pacman by the current position of Pacman
#Pacman's visible range is a 7x7 matrix that Pacman is at the center of the matrix
def Update_Pacman_view(map,current_view, pos):

    x = pos[0] - 3 
    y = pos[1] - 3
    Pacman_view = current_view
    for i in range(7):
        for j in range(7):
            if 0 <= x + i < len(current_view) and 0 <= y + j < len(current_view[0]) : 
                Pacman_view[abs(x+ i)][abs(y+ j)] = map[abs(x + i)][abs(y + j)]
    return Pacman_view

#Handle the situation that Pacman reach the food's position. Update the map, the foods list and the pacman view
def EatFood(map, pacmanpos, foods, pacmanview):

    #Remove the food at index of pacmanpos
    foods.pop(foods.index(pacmanpos))

    #Remove the food from the map and the Pacman view 
    map[pacmanpos[0]][pacmanpos[1]] = 0
    pacmanview[pacmanpos[0]][pacmanpos[1]] = 0
    
    return map, foods, pacmanview

#Function to handle one step-move of Pacman 

def GetNewPath(map, pacman_pos, pacman_view):
     #Find all foods exist in Pacman visibilty
    foods_in_pacman_view = FindObject(pacman_view,2)

    if len(foods_in_pacman_view )== 0: #When there is no more food in Pacman visibility, 
        invisible_pos = FindObject(pacman_view,4) #I find the postion of all invisible positions around Pacman,
                                            #then sort them ascending by the heuristic function
        if len(invisible_pos) != 0: #When Pacman had explored all the map
            invisible_pos = sorted(invisible_pos, key= lambda pos: find_heuristic(pacman_pos,pos), reverse = False)

        #I use A* algorithm to find the path to the nearest position
        #I found in "map" instead of the Pacman view becausse I just want to find a possible next move of Pacman. 
        #The visible range is so small, so in many situation , the goal is block by the bisibility, Pacman could not find the path to it.
        path = a_star_algorithm(map, pacman_pos, invisible_pos[0])

    else: #If food is located in Pacman view, I find the nearest path to food.

        #I find the paths from Pacman to all of food in its visible range
        path_list = []
        for food in foods_in_pacman_view:
            path = a_star_algorithm(map, pacman_pos,food)
            path_list.append(path)
        #Sort the path to find the nearest path
        path_list = sorted( path_list, key = len, reverse = False )
        
        path = path_list[0]

    return path

def find_move_with_largest_distance(possible_moves, monster_pos):
    largest_distance = float('-inf')
    best_move = None

    for move in possible_moves:
        total_distance = 0
        for pos in monster_pos:
            distance = find_heuristic(move, pos)
            total_distance += distance
        if total_distance > largest_distance:
            largest_distance = total_distance
            best_move = move
    return best_move
def PacmanMove(map, pacman_pos, pacman_view):

    #Find all foods exist in Pacman visibilty
    foods_in_pacman_view = FindObject(pacman_view,2)
    monsters_in_pacman_view = FindObject(pacman_view, 3)
    path = GetNewPath(map, pacman_pos, pacman_view)
    next_pos = pacman_pos


    if (len(path) == 0): #Pacman cannot move anymore (there is no foods or invisible position)
            status = "Blocked"
            return next_pos, map, pacman_view
        
    elif (len(path) == 1): # Pacman reach the goal (goal can be food or the nearest invisible position)
                    #In this situation, Pacman is no longer afraid of monsters
        next_pos = path[0] #Pacman move

        pacman_view = Update_Pacman_view(map, pacman_view, next_pos)
        # Pacman_path.append(start_pos) 

        return next_pos, map, pacman_view

    else: #more than 1 step to go to the goal
        current_pos = path.pop(0) # Get the current position of Pacman 
        # if start_pos in foods_pos:
        #     map, foods_pos, pacman_view = EatFood(map, start_pos, foods_pos, pacman_view)
        new_pos = path[0] #Get the next postion in path
        
        movable_pos = get_neighbors(current_pos,map)

        if (new_pos in movable_pos) and (check_safe_move(new_pos, monsters_in_pacman_view) == True): #when Pacmnan is in a safe position with monsters
            
            next_pos = new_pos #Move Pacman to the next position
            #Update the view of Pacman
            pacman_view = Update_Pacman_view(map, pacman_view, next_pos)
            return next_pos, map, pacman_view
    
        else: #When the monsters is near Pacman, Pacman have to change the moving path
            movable_pos = get_neighbors(current_pos, map)

        # movable_pos = sorted(movable_pos, key= lambda pos:find_heuristic(pos))

            for pos in movable_pos:
                    if check_safe_move(pos, monsters_in_pacman_view) == True:
                        next_pos = pos #Pacman move
                        break
            # best_move = find_move_with_largest_distance(movable_pos, monsters_in_pacman_view)

            # if best_move:
            #     next_pos = best_move
            # else:
            #     for pos in movable_pos:
            #         if check_safe_move(pos, monsters_in_pacman_view) == True:
            #             next_pos = pos #Pacman move
            #             break

                    #Update the view of Pacman
            pacman_view = Update_Pacman_view(map, pacman_view, next_pos)

            return next_pos, map, pacman_view

    
        # return []
#Check a position is safe or not
def check_safe_move(pos, monsters_pos):
    for monster in monsters_pos:
        if find_heuristic(pos, monster) <= 1:
            return False
    return True


def Handle_Level_03(map, start):

    start_pos = tuple(start) 
    pacman_view = Init_Pacman_view(map)
    pacman_view = Update_Pacman_view(map, pacman_view, start_pos)
    foods_pos = FindObject(map,2)
    monsters_pos = FindObject(map,3)

    #Pacman path and monster path
    Pacman_path = [start_pos]
    Monster_path = [monsters_pos]
    #Set the default status
    status = "Win"
    while (True):
        foods_pos = FindObject(map,2)
        if (start_pos in monsters_pos):
            print (" +++++++ GAME OVER ++++++++++")
            status = "Lose condition 1"
            print (start_pos)
            print (status)
            return Pacman_path, Monster_path,status
        #Monsters will move first
        monsters_pos, map = MonsterMove(map, monsters_pos)
        Monster_path.append(monsters_pos)
        pacman_view = Update_Pacman_view(map, pacman_view, start_pos)
        
        if (start_pos in monsters_pos):
            print (" +++++++ GAME OVER ++++++++++")
            print (start_pos)
            status = "Lose condition 2"
            return Pacman_path, Monster_path,status
        
        if (len(foods_pos) == 0):
            print ("++++++++++ WIN +++++++++++++++")
            status = "win"
            print (start_pos)
            return Pacman_path, Monster_path,status

        #Pacman will move one step, I use Pacmanmove funciton to determine which position Pacman will move to
        start_pos, map, pacman_view= PacmanMove (map, start_pos, pacman_view)
        Pacman_path.append(start_pos)

        if (start_pos in monsters_pos):
            print (" +++++++ GAME OVER ++++++++++")
            print (start_pos)
            status = "Lose condition 2"
            return Pacman_path, Monster_path,status
        if start_pos in foods_pos:
            map, foods_pos, pacman_view = EatFood(map, start_pos, foods_pos, pacman_view)

        pacman_view = Update_Pacman_view(map, pacman_view,start_pos)

        
    return Pacman_path, Monster_path, status




