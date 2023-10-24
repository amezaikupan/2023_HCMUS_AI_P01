import pygame

#Read size, map and position of pacman from txt file
def readMap(fileName):
    try:
        size = ()
        map = []
        position = []
        
        with open(fileName, "r") as file:
            size = file.readline()
            size = tuple(int(size.split()))
            res = file.readlines()
            #Read map and pos
            for i in range(len(res)):
                map.append(int(res[i].split()))
            position = map.pop(-1)    
            print(size, map, position)

    except FileNotFoundError:
        print("Could not open file")
    except Exception as e:
        print("Error reading Map")
        
path = f"../test/lv1_map1.txt"
readMap(path)