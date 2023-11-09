from algorithm.Level3 import Handle_Level_03
from algorithm.Level1 import Handle_level_01
from algorithm.Level2 import Handle_level_02
from algorithm.minimax_algorithm import run

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
    gameEndState, pacman_path, monster_path = run(pacmanPos, map)
    status = None
    return pacman_path, monster_path, status