#Read size, map and position of pacman from txt file
def readMap(filename):
    try:
        with open(filename, "r") as f:
            # Read the size and convert to a tuple
            size = tuple(map(int, f.readline().split()))

            # Read the map data and convert to a list of lists
            map_data = [list(map(int, line.split())) for line in f]

            # Extract the position from the last row
            pos = map_data.pop()
            return size, map_data, pos
    except FileNotFoundError:
        print("Could not open file")
    except Exception as e:
        print(e)
        
def calculateCoor(in_coords, in_size):
    return in_coords[1] * in_size, in_coords[0] * in_size
