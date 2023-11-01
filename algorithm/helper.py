def get_map(file_name):
    file = open(file_name, "r")
    size = []
    map = []
    start_pos = []

    line = file.readline()
    size = tuple(int(i) for i in line.split())

    for line in file:
        row = []
        
        for x in line.split(): 
            row .append(int(x))
        map.append(row)

    start_pos = map.pop(-1)

    return map, size, start_pos


