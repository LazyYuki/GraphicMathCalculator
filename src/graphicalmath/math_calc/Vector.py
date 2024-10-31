class Vector3d:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def nullVectorList(self):
        return [0, 0, 0, self.x, self.y, self.z]

    def toList(self):
        return [self.x, self.y, self.z]