#The heuristic function is the distance between the start position and goal position
def find_heuristic (start, goal):
    distance = ((start[0] - goal[0])**2 + (start[1] - goal[1])**2)**0.5
    return distance

#Function to find the position of food in map
def find_food(map):
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 2:
                return (i,j)
            
#Function to find all the neighbors of a position in map
#A valid neighbor is a position located in the map and to the left, down, up, or right of the origin position
def get_neighbors(pos, map):

    x,y = pos
    neighbors = []

    #Find the position of neighbor in left, down, up, right side
    candidate_neighbors = [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]

    for candidate in candidate_neighbors:
        x = candidate[0]
        y = candidate[1]

        #Check the candidate is in the map, is the food or path.
        if( 0 <= x < len(map) and 0 <= y < len(map[0])  and (map[x][y] in (0,2,3)) ):
                neighbors.append((x,y)) # If true, it is a valid neighbor.

    return neighbors

def a_star_algorithm(map, start, goal):
    start_pos = tuple(start)
    food_pos = tuple(goal)

    total_cost = 0

    #A prioriry queue
    frontier = [(start_pos, total_cost)]
    #List of position explored
    explored = set()

    #Store the previous position of a position using a dicitonary
    previous_pos = {}
    path = [] #Path

    while frontier:
        #Get the current position and its total cost
        current_pos, total_cost = frontier.pop(0)

        #When pacman reach the food position
        if current_pos == food_pos:
            #Trace back the road to from current position to its preveious position
            while current_pos in previous_pos:
                path.append(current_pos)
                current_pos = previous_pos[current_pos]
            path.append(current_pos)

            #Reverse the path 
            return path[::-1]
            
        if current_pos not in explored:
            explored.add(current_pos)

            for neighbor in get_neighbors(current_pos, map):
                
                if neighbor not in explored:
                    new_total_cost = total_cost + 1 
                    previous_pos[neighbor] = current_pos
                    frontier.append((neighbor,new_total_cost))
        
            frontier.sort(key = lambda x: x[1] + find_heuristic(x[0],food_pos), reverse = False)

     #Trace back the road to from current position to its preveious position
    while current_pos in previous_pos:
        path.append(current_pos)
        current_pos = previous_pos[current_pos]
    path.append(current_pos)
    #Reverse the path 
    return path[::-1]


