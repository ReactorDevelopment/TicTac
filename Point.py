#simple class to store a point
class Point:

    def __init__(self):
        self.x = 0.0
        self.y = 0.0

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point: " + str(self.x) + ", " + str(self.y)
