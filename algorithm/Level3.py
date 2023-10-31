from A_star import find_heuristic,get_neighbors, a_star_algorithm
from helper import get_map
import random
import copy

#Find all the position in the map for all types of object
def FindObject(map, type):
    pos_list = []
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == type:
                pos_list.append((i,j))
    return pos_list

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
            #Check the pos is in the map, is the food or path.
            if( 0 <= x < len(map) and 0 <= y < len(map[0])  and map[x][y] != 1):
                valid_pos.append((x,y)) # If true, it is a valid position.
        move = random.choice(valid_pos)
       
        map[move[0]][move[1]] = 3
        map[monster[0]][monster[1]] = 0
        MonstersPos.append(move)
    return MonstersPos,map

#Because in level 3, pacman has a visible range, so I change all the value of map into another value (specically 4)
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

    #Remove the food at index is the pacmanpos
    foods.pop(foods.index(pacmanpos))

    #Remove the food from the map and the Pacman view
    map[pacmanpos[0]][pacmanpos[1]] = 0
    pacmanview[pacmanpos[0]][pacmanpos[1]] = 0
    
    return map, foods, pacmanview

#Function to handle one step-move of Pacman
def PacmanMove(map, pacman_pos, monsters, pacman_view):

    #Find all foods exist in Pacman visibilty
    foods_in_pacman_view = FindObject(pacman_view,2)
    print ("Food in pacman view:")
    print (foods_in_pacman_view)

    if len(foods_in_pacman_view )== 0: #When there is no more food in Pacman visibility, 
        invisible_pos = FindObject(pacman_view,4) #I find the postion of all invisible positions around Pacman,
                                            #then sort them ascending by the heuristic function
        
        if len(invisible_pos) == 0: #When the Pacman had explored all the map
            return []
        
        invisible_pos = sorted(invisible_pos, key= lambda pos: find_heuristic(pacman_pos,pos))
        
        if (invisible_pos[0] in monsters):
            invisible_pos.pop(0)
        print ("invisible: next pos")
        print(invisible_pos[0])

        #I use A* algorithm to find the path to the nearest position
        #I found in "map" instead of the Pacman view becausse I just want to find a possible next step of Pacman. 
        #The visible range is so small, so in many situation , the goal is block by the bisibility, Pacman could not find the path to it.
        path_01 = a_star_algorithm(map, pacman_pos, invisible_pos[0])
    
        return path_01

    else: #If food is located in Pacman view, I find the path to the nearest food.

        foods_in_pacman_view = sorted(foods_in_pacman_view, key=lambda food: find_heuristic(pacman_pos, food))
        path_02 = a_star_algorithm(map, pacman_pos, foods_in_pacman_view[0])
        return path_02
        
def check_safe_move(pos, monsters_pos):
    for monster in monsters_pos:
        if find_heuristic(pos, monster) <= 1:
            return False
    return True
def create_pure_map(map):
    rows = len(map)
    cols = len(map[0])

    pure_map = [[0 for _ in range(cols)] for _ in range(rows)]
    
    for i in range(rows):
        for j in range(cols):
            if map[i][j] == 1:
                pure_map[i][j] = 1
    
    return pure_map
def Handle_Level_03(map, start):

    start_pos = tuple(start) 
    pure_map = create_pure_map(map)
    pacman_view = Init_Pacman_view(map)
    pacman_view = Update_Pacman_view(map, pacman_view, start_pos)
    print ("+++++++++++")

    monsters_pos = FindObject(map,3)
    foods_pos = FindObject(map,2)
    Pacman_path = [start_pos]
    Monster_path = [monsters_pos]
    print ("So luong food:", foods_pos)
    while (True):
        foods_pos = FindObject(map,2)
        print ("+++++++++++++++++++++++++++++++")

        print ("Start position:")
        print (start_pos)
        #Get a possible path of  Pacman
        path = PacmanMove (pure_map, start_pos,monsters_pos, pacman_view)
        print ("path")
        print (path)
        if (len(path) == 0): #Pacman cannot move anymore (there is no foods or invisible position)
            for line in pacman_view:
                print (line)
            print ("++++++++")
            for line in map:
                print (line)
            print ("CANNOT MOVE ANYMORE")
            print (foods_pos)
            return Pacman_path, Monster_path
        
        if (len(path) == 1): # Pacman reach the goal (goal can be food or the nearest invisible position)
                            #In this situation, Pacman is no longer afraid of monsters
            monsters_pos, map = MonsterMove(map, monsters_pos)
            print ("Monster positon: ", monsters_pos)
            Monster_path.append(monsters_pos)
            start_pos = path[0] #Get the goal
            map, foods_pos, pacman_view = EatFood(map, start_pos, foods_pos, pacman_view)
            
            pacman_view = Update_Pacman_view(map, pacman_view, start_pos)
            Pacman_path.append(start_pos)

            print ("So luong food hien tai: ", len(foods_pos))

        else: #more than 1 step to go to the goal
            start_pos = path.pop(0) # Get the current position of Pacman 
            next_pos = path[0] #Move Pacman one step to the goal
            #Get the movable position around  
            movable_pos = get_neighbors(start_pos,pacman_view)
            
            if next_pos in movable_pos and  check_safe_move(next_pos, monsters_pos) == True: #when Pacmnan is in a safe position with monsters
                start_pos = next_pos #Move Pacman to the next position
                #After that, all the monsters move
                monsters_pos, map = MonsterMove(map, monsters_pos)
                print ("Monster positon: ", monsters_pos)
                Monster_path.append(monsters_pos)
                #Update the view of Pacman
                pacman_view = Update_Pacman_view(map, pacman_view, start_pos)
                Pacman_path.append(start_pos)
            else: #When the monsters is near Pacman, Pacman have to change the moving path
                movable_pos = get_neighbors(start_pos,pacman_view)

                for pos in movable_pos:
                    if check_safe_move(pos, monsters_pos) == True:
                        start_pos = pos
                    break
                #After Pacman move, monsters move
                monsters_pos, map = MonsterMove(map, monsters_pos)
                Monster_path.append(monsters_pos)
                print ("Monster positon: ", monsters_pos)
                Monster_path.append(monsters_pos)
               
                if start_pos in foods_pos:
                    map, foods_pos, pacman_view  = EatFood(map,start_pos, foods_pos, pacman_view)
                    print ("So luong food hien tai: ", len(foods_pos))

                pacman_view = Update_Pacman_view(map, pacman_view, start_pos)
                Pacman_path.append(start_pos)

                if (start_pos in monsters_pos):
                    print (" +++++++ GAME OVER ++++++++++")
                    return Pacman_path, Monster_path

        if (len(foods_pos) == 0):
            print ("++++++++++WIN+++++++++++++++")
            break;
    return Pacman_path, Monster_path


map , size, pos= get_map("../test/lv3_map1.txt")

for line in map:
    print (line)
start_pos = tuple(pos) 

pacman_view = Init_Pacman_view(map)
pacman_view = Update_Pacman_view(map, pacman_view, start_pos)

# start = (16, 18)
# goal = (9, 17)
# path_01 = a_star_algorithm(map, start, goal)
# print (path_01)
Pacman_path, monster_path = Handle_Level_03(map, pos)

print ("Pacman path:")
print (Pacman_path)
print (len(Pacman_path))
print ("Monsters path:")
print (monster_path)
print (len(monster_path))

