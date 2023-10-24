import pygame

#Read size, map and position of pacman from txt file
def readMap(filename):
    try:
        with open(filename, "r") as f:
            # Read the size and convert to a tuple
            size = tuple(map(int, f.readline().split()))

            # Read the map data and convert to a list of lists
            map = [list(map(int, line.split())) for line in f]

            # Extract the position from the last row
            pos = map.pop()
            return size, map, pos
    except FileNotFoundError:
        print("Could not open file")
    except Exception as e:
        print("Error reading Map")
        
path = f"../test/lv1_map1.txt"
readMap(path)