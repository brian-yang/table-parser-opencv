class Table:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.joints = None

    def __str__(self):
        return "(%d, %d, %d, %d)" % (self.x, self.x + self.w, self.y, self.y + self.h)
