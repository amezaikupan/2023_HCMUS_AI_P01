from algorithm.Level3 import Handle_Level_03
from algorithm.Level1 import Handle_level_01
from algorithm.Level2 import Handle_level_02
import algorithm.level4_01 
import algorithm.level4_02

def handleLv1(map, pacmanPos):
    pacman_path = Handle_level_01(map, pacmanPos)
    monster_path = []
    status = None
    print (pacman_path)
    return pacman_path, monster_path, status

def handleLv2(map, pacmanPos):
    pacman_path = Handle_level_02(map, pacmanPos)
    monster_path = []
    status = None
    return pacman_path, monster_path, status

def handleLv3(map, pacmanPos):
    pacman_path, monster_path, status = Handle_Level_03(map, pacmanPos)
    return pacman_path, monster_path, status

def handleLv4(map, pacmanPos):
    algorithm = input("Algorithm (1/2)?")
    if algorithm == 1:
        pacman_path, monster_path, status = algorithm.level4_01.run(pacmanPos, map)
    else:
        pacman_path, monster_path, status = algorithm.level4_02.run(pacmanPos, map)

    return pacman_path, monster_path, status