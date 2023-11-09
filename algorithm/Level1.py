from algorithm.a_star import find_heuristic,get_neighbors, a_star_algorithm,find_food

def Handle_level_01(map, start):
    start_pos = tuple(start)
    goal = find_food(map)
    status = "win"
    Pacman_path = [start_pos]
    Pacman_path = a_star_algorithm(map,start_pos, goal)
    return Pacman_path