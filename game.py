import tkinter

from game_objects.base import Paddle, Brick, Ball, GameObject


class Game(tkinter.Frame):
    _DEFAULT_BALL_RADIUS = 10
    _DEFAULT_PADDLE_WIDTH = 80
    _DEFAULT_PADDLE_HEIGHT = 10
    _SCREEN_WIDTH = 610
    _SCREEN_HEIGHT = 400

    def __init__(self, master: tkinter.Tk):
        super(Game, self).__init__(master)
        self.lives = 3
        self.width = Game._SCREEN_WIDTH
        self.height = Game._SCREEN_HEIGHT
        self.canvas = tkinter.Canvas(self, bg='#000000', width=self.width, height=self.height)
        self.canvas.pack()
        self.pack()

        self.items = {}
        self.ball = None
        self.paddle = Paddle(self.canvas,
                             Game._DEFAULT_PADDLE_WIDTH,
                             Game._DEFAULT_PADDLE_HEIGHT,
                             int(self.width / 2),
                             326,
                             GameObject.DEFAULT_COLOR)
        self.items[self.paddle.item] = self.paddle
        for x in range(5, self.width - 5, 75):
            self.add_brick(x + 37.5, 50, 2)
            self.add_brick(x + 37.5, 70, 1)
            self.add_brick(x + 37.5, 90, 1)

        self.hud = None
        self.setup()
        self.canvas.focus_set()
        self.canvas.bind('<Left>', lambda _: self.paddle.move(-10))
        self.canvas.bind('<Right>', lambda _: self.paddle.move(10))

    def add_brick(self, x, y, hits):
        brick = Brick(self.canvas, x, y, hits)
        self.items[brick.item] = brick

    def add_ball(self):
        if self.ball is not None:
            self.ball.delete()
        paddle_coords = self.paddle.get_position()
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
        self.ball = Ball(self.canvas, Game._DEFAULT_BALL_RADIUS, x, 310, GameObject.DEFAULT_COLOR)
        self.paddle.set_ball(self.ball)

    def draw_text(self, x: int, y: int, text: str, size=40):
        font = ('Helvetica', size)
        return self.canvas.create_text(x, y, text=text, font=font, fill=GameObject.DEFAULT_COLOR)

    def update_lives_text(self):
        text = 'Lives: {}'.format(self.lives)
        if not self.hud:
            self.hud = self.draw_text(50, 20, text, size=15)
        else:
            self.canvas.itemconfig(self.hud, text=text)

    def check_collisions(self):
        ball_coords = self.ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items if x in self.items]
        self.ball.collide(objects)

    def start(self):
        self.canvas.unbind('<space>')
        self.canvas.delete(self.text)
        self.paddle.ball = None
        self.game_loop()

    def game_loop(self):
        self.check_collisions()
        num_bricks = len(self.canvas.find_withtag('brick'))
        if num_bricks == 0:
            self.ball.speed = None
            self.draw_text(300, 200, 'You Win!')
        elif self.ball.get_position()[3] >= self.height:
            self.ball.speed = None
            self.lives = -1
            if self.lives < 0:
                self.draw_text(300, 200, 'Game Over')
            else:
                self.after(1000, self.setup)
        else:
            self.ball.update()
            self.after(50, self.game_loop)

    def setup(self):
        self.add_ball()
        self.update_lives_text()
        self.text = self.draw_text(300, 200, 'Press Space to start...')
        self.canvas.bind('<space>', lambda _: self.start())


if __name__ == '__main__':
    root = tkinter.Tk()
    root.title('Arkanoid')
    game = Game(root)
    game.mainloop()
