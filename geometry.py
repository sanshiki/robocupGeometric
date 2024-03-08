import math

class GeoObj:
    def __init__(self):
        pass


class GeoPoint(GeoObj):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            self.x = args[0][0]
            self.y = args[0][1]
        elif len(args) == 2:
            self.x = args[0]
            self.y = args[1]
        else:
            raise ValueError
        
    def __add__(self, vector):
        new_x = self.x + math.cos(vector.dir) * vector.mod
        new_y = self.y + math.sin(vector.dir) * vector.mod
        return GeoPoint(new_x, new_y)

    def __sub__(self, other):
        if type(other) == GeoPoint:
            direction = math.atan2(self.y - other.y, self.x - other.x)
            length = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
            return GeoVector(self.x - other.x, self.y - other.y, direction, length)
        elif type(other) == tuple and len(other) == 2:
            direction = math.atan2(self.y - other[1], self.x - other[0])
            length = math.sqrt((self.x - other[0]) ** 2 + (self.y - other[1]) ** 2)
            return GeoVector(self.x - other[0], self.y - other[1], direction, length)

    def __eq__(self, other):
        if type(other) == GeoPoint:
            return self.x == other.x and self.y == other.y
        elif type(other) == tuple and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        else:
            return False

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError

    def __len__(self):
        return 2

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __neg__(self):
        return GeoPoint(-self.x, -self.y)

    def __pos__(self):
        return GeoPoint(self.x, self.y)
    
    # turn into tuple
    def __iter__(self):
        return (self.x, self.y).__iter__()
    
    def __str__(self) -> str:
        display_x = round(self.x, 2)
        display_y = round(self.y, 2)
        return f'({display_x}, {display_y})'
    

class GeoVector(GeoObj):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 2:
            self.x = args[0]
            self.y = args[1]
            self.dir = math.atan2(self.y, self.x)
            self.mod = math.sqrt(self.x ** 2 + self.y ** 2)
        elif len(args) == 4:
            self.x = args[0]
            self.y = args[1]
            self.dir = args[2]
            self.mod = args[3]
        else:
            raise ValueError

    def __add__(self, other):
        return GeoVector(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar):
        return GeoVector(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        return GeoVector(self.x / scalar, self.y / scalar)
    
    
        
    def mod(self):
        return self.mod
    

def Polar2Vector(dir, mod):
    return GeoVector(math.cos(dir) * mod, math.sin(dir) * mod)


def isPointOnLine(point, start, end, buffer=2):
    if (start - point).mod + (end - point).mod - (start - end).mod <= buffer:
        return True
    return False