class Ball:

    def __init__(self, r, (x, y)):
        self.r = r
        self.x, self.y = x, y
        self.xv, self.yv = 0, 0

    def __repr__(self):
        return "<Ball. r: {}, x: {}, y: {}, xv: {}, yv: {}>".format(
                self.r, self.x, self.y, self.xv, self.yv)

    def move(self):
        self.x += self.xv
        self.y += self.yv

    def accelerate(self, (gx, gy)):
        self.xv += gx
        self.yv += gy
