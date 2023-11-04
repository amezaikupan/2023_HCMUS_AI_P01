class Measure():
    def getDistanceBetween2Points(point1, point2):
        distance = ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5
        # print("Distance: " + str(distance))
        return distance
        