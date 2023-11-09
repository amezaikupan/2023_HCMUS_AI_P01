from algorithm.Level3 import Handle_Level_03
import algorithm.level_04_algorithm_02 
import algorithm.level_04_algorithm_01

def handleLv1(map, pacmanPos):
    pacman_path = [(10, 2), (9,2), (8,2), (7,2), (6,2), (6,3), (5, 3), (4, 3), (3, 3), (2, 3), (1, 3), (1,4), (1, 5), (1, 6), (2, 6), (3, 6), 
(4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10), (9,10), (8,10)]
    monster_path = []
    status = None
    return pacman_path, monster_path, status

def handleLv2(map, pacmanPos):
    return None

def handleLv3(map, pacmanPos):
    pacman_path, monster_path, status = Handle_Level_03(map, pacmanPos)
    return pacman_path, monster_path, status

def handleLv4(map, pacmanPos):
    mode = input("Mode (1/2)?")
    if mode == 1:
        pacman_path, monster_path, status = algorithm.level_04_algorithm_01.run(pacmanPos, map)
    else:
        pacman_path, monster_path, status = algorithm.level_04_algorithm_02.run(pacmanPos, map)

    return pacman_path, monster_path, status