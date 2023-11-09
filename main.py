import pygame
import time
from graphic.util import calculateCoor
from graphic.gameObject import Wall, Pacman, Monster, Food, GameController, Environment
CELL_SIZE = 40

if __name__ == '__main__':
    level = input("Level: ")
    map = input("Map: ")
    path = f"test/lv{level}_map{map}.txt"
    
    #Get intitial positions of pacman, monsters, food and walls
    controller = GameController(path)
    # print("Map: ", controller._map)
    # print("Size: ", controller._size)
    # print("Food: ", controller._food_positions)
    # print("Monster: ", controller._monster_spawns)
    # print("Pacman: ", controller._pacmanPos)
    # print("Wall: ", controller._wall_positions)
    # print("Empty space: ", controller._reachable_positions)
    
    #Initialize game environment
    environment = Environment(controller._size[1] * CELL_SIZE, controller._size[0] * CELL_SIZE)
    
    #Get path from search algorithms
    start_point = time.time()
    pacman_path, monsters_path, status = controller._pathFinder.get_path(level)
    path_calculation_time = time.time() - start_point
    print("Path calculation time: ", path_calculation_time)
    
    #Graphic render
    #Initialize wall:
    for pos in controller._wall_positions:
        environment.setWall(Wall(pos[1], pos[0], CELL_SIZE, environment, f"assets/wall.png"))
        
    #Initialize food:
    for food_pos in controller._food_positions:
        environment.setFood(Food(food_pos[1] * CELL_SIZE, food_pos[0] * CELL_SIZE, CELL_SIZE, environment, f"assets/food.png"))
        
    #Initialize monsters:
    for pos, monster_pos in enumerate(controller._monster_spawns):
        monster_path = [calculateCoor(sublist[pos]) for sublist in monsters_path]

        monster = Monster(
            controller._monster_spawns[pos][1] * CELL_SIZE, 
            controller._monster_spawns[pos][0] * CELL_SIZE,
            CELL_SIZE,
            environment,
            f"assets/ghost.png",
            monster_path,
            controller
        )
        environment.setMonster(monster)
      
    #Initialize pacman:
    pacman_path = [calculateCoor(item) for item in pacman_path]
    pacman = Pacman(
        controller._pacmanPos[1] * CELL_SIZE,
        controller._pacmanPos[0] * CELL_SIZE,
        CELL_SIZE,
        environment,
        f"assets/pacman.png",
        pacman_path,
        controller
    )
    environment.setPacman(pacman)
    
    #Game start
    environment.setLevel(level)
    environment.setMap(map)
    environment.start()
 
    
    