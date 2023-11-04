from algorithm.Level3 import Handle_Level_03

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
    pacman_path = [(9, 10), (9, 11), (9, 12), (9, 13), (8, 13), (7, 13), (6, 13), (5, 13), (5, 14), (5, 15), (5, 16), (6, 16), (7, 16), (7, 
15), (7, 14), (7, 13), (7, 12), (7, 11), (7, 10), (7, 9), (7, 8), (7, 7), (7, 6), (8, 6), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10), (9, 11), (9, 12), (9, 13), (8, 13), (7, 13), (7, 14), (7, 15), (8, 15), (9, 15), (9, 16), (9, 17), (9, 18), (8, 18), (7, 18), (6, 18), (5, 18), (5, 17), (5, 16), (4, 16), (3, 16), (3, 15), (3, 14), (3, 13), (4, 13), (5, 13), (5, 14), (5, 15), (5, 16), (5, 17), (5, 18), (4, 18), (3, 18), (2, 18), (1, 18), (1, 17), (1, 16), (1, 15), (2, 15), (3, 15), (3, 14), (3, 13), (3, 12), (3, 11), (3, 10), (3, 9), (3, 8), (3, 7), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (7, 5), (7, 4), (8, 4), (9, 4), (9, 3), (9, 2), (9, 1), (8, 1), (7, 1), (6, 1), (5, 1), (5, 2), (5, 3), 
(5, 4), (5, 5), (5, 6), (4, 6), (3, 6), (3, 5), (3, 4), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (6, 9), (6, 10), (5, 10), (4, 10), (3, 10), (3, 11), (3, 12), (3, 13), (2, 13), (1, 13), (1, 12), (1, 11), (1, 10), (1, 9), (1, 8), (1, 7), (1, 6), (2, 6), (3, 6), (3, 5), (3, 4), (2, 4), (1, 4), (1, 3), (1, 2), (1, 1), (2, 1), (3, 1), (4, 1)]
    monster_path = [[(5, 9), (5, 10)], [(4, 9), (5, 9)], [(4, 10), (5, 10)], [(5, 10), (6, 10)], [(6, 10), (7, 10)], [(7, 10), (7, 11)], [(7, 11), (7, 
12)], [(7, 12), (7, 13)], [(7, 13), (6, 13)], [(6, 13), (5, 13)], [(5, 13), (5, 14)], [(5, 14), (5, 15)], [(5, 15), (5, 16)], [(5, 16), (6, 16)], [(6, 16), (7, 16)], [(7, 16), (7, 15)], [(7, 15), (7, 14)], [(7, 14), (7, 13)], [(7, 13), (7, 12)], [(7, 12), (7, 11)], [(7, 11), (7, 10)], [(7, 10), (7, 9)], [(7, 9), (7, 8)], [(7, 8), (7, 7)], [(7, 7), (7, 6)], [(7, 6), (8, 6)], [(8, 6), (9, 6)], [(9, 6), (9, 7)], [(9, 7), (9, 8)], [(9, 8), (9, 9)], [(9, 9), (9, 10)], [(9, 10), (9, 11)], [(9, 11), (9, 12)], [(9, 12), (9, 13)], [(9, 13), (8, 13)], [(8, 13), (7, 13)], [(7, 13), (7, 14)], [(7, 14), (7, 15)], [(7, 15), (8, 15)], [(8, 15), (9, 15)], [(9, 15), (9, 16)], [(9, 16), (9, 17)], [(9, 17), (9, 18)], [(9, 18), (8, 18)], [(8, 18), (7, 18)], [(7, 18), (6, 18)], [(6, 18), (5, 18)], [(5, 18), (5, 17)], [(5, 17), (5, 16)], [(5, 16), (4, 16)], [(4, 16), (3, 16)], [(3, 16), (3, 15)], [(3, 15), (3, 14)], [(3, 14), (3, 13)], [(3, 13), (4, 13)], [(4, 13), (5, 13)], [(5, 
13), (5, 14)], [(5, 14), (5, 15)], [(5, 15), (5, 16)], [(5, 16), (5, 17)], [(5, 17), (5, 18)], [(5, 18), (4, 18)], [(4, 18), (3, 18)], [(3, 18), (2, 18)], [(2, 18), (1, 18)], [(1, 18), (1, 17)], [(1, 17), (1, 16)], [(1, 16), (1, 15)], [(1, 15), (2, 15)], [(2, 15), (3, 15)], [(3, 15), (3, 14)], [(3, 14), (3, 13)], [(3, 13), (3, 12)], [(3, 12), (3, 11)], [(3, 11), (3, 10)], [(3, 10), (3, 9)], [(3, 9), (3, 8)], [(3, 
8), (3, 7)], [(3, 7), (3, 6)], [(3, 6), (4, 6)], [(4, 6), (5, 6)], [(5, 6), (6, 6)], [(6, 6), (7, 6)], [(7, 6), (7, 5)], [(7, 5), (7, 4)], 
[(7, 4), (8, 4)], [(8, 4), (9, 4)], [(9, 4), (9, 3)], [(9, 3), (9, 2)], [(9, 2), (9, 1)], [(9, 1), (8, 1)], [(8, 1), (7, 1)], [(7, 1), (6, 
1)], [(6, 1), (5, 1)], [(5, 1), (5, 2)], [(5, 2), (5, 3)], [(5, 3), (5, 4)], [(5, 4), (5, 5)], [(5, 5), (5, 6)], [(5, 6), (4, 6)], [(4, 6), (3, 6)], [(3, 6), (3, 5)], [(3, 5), (3, 4)], [(3, 4), (3, 3)], [(3, 3), (4, 3)], [(4, 3), (5, 3)], [(5, 3), (6, 3)], [(6, 3), (7, 3)], [(7, 3), (7, 4)], [(7, 4), (7, 5)], [(7, 5), (7, 6)], [(7, 6), (7, 7)], [(7, 7), (7, 8)], [(7, 8), (7, 9)], [(7, 9), (6, 9)], [(6, 9), (6, 10)], [(5, 9), (5, 10)], [(4, 9), (4, 10)], [(3, 9), (3, 10)], [(3, 10), (3, 11)], [(3, 11), (3, 12)], [(3, 12), (3, 13)], [(3, 13), (2, 13)], [(2, 13), (1, 13)], [(1, 13), (1, 12)], [(1, 12), (1, 11)], [(1, 11), (1, 10)], [(1, 10), (1, 9)], [(1, 9), (1, 8)], [(1, 8), (1, 7)], [(1, 7), (1, 6)], [(1, 6), (2, 6)], [(2, 6), (3, 6)], [(3, 6), (3, 5)], [(3, 5), (3, 4)], [(3, 4), (2, 4)], [(2, 4), (1, 4)], [(1, 4), (1, 3)], [(1, 3), (1, 2)], [(1, 2), (1, 1)], [(1, 1), (2, 1)], [(2, 1), (3, 1)]]
    status = None
    return pacman_path, monster_path, status