import tkinter


class GameObject:
    DEFAULT_COLOR = 'white'

    def __init__(self, canvas: tkinter.Canvas, item, color):
        self.canvas = canvas
        self.item = item
        self.color = color

    def get_position(self) -> list:
        return self.canvas.coords(self.item)

    def move(self, x: int, y: int):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)

    def set_color(self, color):
        self.color = color
        self.canvas.itemconfig(self.item, fill=color)


class Ball(GameObject):
    def __init__(self, canvas: tkinter.Canvas, radius: int, x: int, y: int, color: str):
        self.radius = radius
        self.direction = [1, -1]
        self.speed = 10
        ball = canvas.create_oval(x - self.radius,
                                  y - self.radius,
                                  x + self.radius,
                                  y + self.radius,
                                  fill=color,
                                  tags='ball')
        super().__init__(canvas, ball, color)

    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
        if coords[1] <= 0:
            self.direction[1] *= -1
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        self.move(x, y)

    def collide(self, game_objects):
        coords = self.get_position()
        x = (coords[0] + coords[2]) * 0.5
        if len(game_objects) > 1:
            self.direction[1] *= -1
        elif len(game_objects) == 1:
            game_object = game_objects[0]
            go_coords = game_object.get_position()
            if x > go_coords[2]:
                self.direction[0] = 1
            elif x < go_coords[0]:
                self.direction[0] = -1
            else:
                self.direction[1] *= -1

        for go in game_objects:
            if isinstance(go, Brick):
                go.hit()


class Paddle(GameObject):
    def __init__(self, canvas: tkinter.Canvas, width: int, height: int, x: int, y: int, color: str):
        self.width = width
        self.height = height
        self.ball = None
        paddle = canvas.create_rectangle(x - self.width / 2,
                                         y - self.height / 2,
                                         x + self.width / 2,
                                         y + self.height / 2,
                                         fill=color,
                                         tags='paddle')
        super().__init__(canvas, paddle, color)

    def set_ball(self, ball: Ball):
        self.ball = ball

    def move(self, offset: int, **kwargs):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            super().move(offset, 0)
            if self.ball:
                self.ball.move(offset, 0)


class Brick(GameObject):
    COLORS = {
        1: '#999999',
        2: '#555555',
        3: '#222222'
    }
    WIDTH = 75
    HEIGHT = 20

    def __init__(self, canvas: tkinter.Canvas, x, y, hits):
        self.width = Brick.WIDTH
        self.height = Brick.HEIGHT
        self.hits = hits
        self.color = Brick.COLORS[hits]
        brick = canvas.create_rectangle(x - self.width / 2,
                                        y - self.height / 2,
                                        x + self.width / 2,
                                        y + self.height / 2,
                                        fill=self.color,
                                        tags='brick')
        super().__init__(canvas, brick, Brick.COLORS[hits])

    def hit(self):
        self.hits -= 1
        if self.hits == 0:
            self.delete()
        else:
            self.canvas.itemconfig(self.item, fill=Brick.COLORS[self.hits])
