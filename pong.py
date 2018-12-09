import random
import math
# import pgz

WIDTH = 1000
HEIGHT = 700

# ---------------------- BALL CLASS ---------------------
class BallClass:
    def __init__(self):
        self.position = [WIDTH/2, HEIGHT/2]
        if random.random() < 0.5:  # choose random starting angle
            self.angle = random.randint(-40, 40)
        else:
            self.angle = random.randint(140, 220)
        self.velocity = 8  # ball initial velocity
        self.size = 20  # ball size
        self.rect = Rect((self.position[0] - self.size/2, self.position[1] - self.size/2), (self.size, self.size))     
    
    def update_ball(self):  # how to update ball between frame
        self.position = [self.position[0] + math.cos(math.radians(self.angle)) * self.velocity, self.position[1] - math.sin(math.radians(self.angle)) * self.velocity]
        self.rect = Rect((self.position[0] - self.size/2, self.position[1] - self.size/2), (self.size, self.size))
        self.velocity += 0.02
        
        if self.position[1] + self.size/2 > HEIGHT:  # Ball hit the bottom
            self.angle = 360 - self.angle
            sounds.ping_pong_8bit_plop.play(0, 300)
        
        if self.position[1] - self.size/2 < 0:  # Ball hit the top       
            self.angle = 360 - self.angle
            sounds.ping_pong_8bit_plop.play(0, 300)
        
        if self.position[0] < 80 and math.cos(math.radians(self.angle)) < 0:  # ball reach left paddle right side from the right
            if self.position[1] > (game.PADDLE1_Y - game.PADDLESIZE/2) \
            and self.position[1] < (game.PADDLE1_Y + game.PADDLESIZE/2) \
            and self.position[0] - 60 > 0:
                if self.position[1] - 20 < (game.PADDLE1_Y - game.PADDLESIZE/2):  # left paddle, top tip
                    self.angle = 180 - self.angle + 20
                elif self.position[1] + 20 > (game.PADDLE1_Y + game.PADDLESIZE/2):  # left paddle, bottom tip
                    self.angle = 180 - self.angle - 20
                else:  # left paddle center
                    self.angle = 180 - self.angle
                sounds.ping_pong_8bit_beeep.play(0, 300)
            else:
                if self.position[0] < - 20:  # ball is out of screen on the left
                    sounds.ping_pong_8bit_peeeeeep.play(0, 300)
                    game.playingball = False
                    game.scoreP2 += 1
        
        if self.position[0] + 10 > WIDTH - 70 and math.cos(math.radians(self.angle)) > 0: # ball reach right paddle left side from the left
            if self.position[1] + 10 > (game.PADDLE2_Y - game.PADDLESIZE/2) \
            and self.position[1] + 10 < (game.PADDLE2_Y + game.PADDLESIZE/2) \
            and self.position[0] + 40 < WIDTH:
                if self.position[1] - 20 < (game.PADDLE2_Y - game.PADDLESIZE/2):  # left paddle, top tip
                    self.angle = 180 - self.angle - 20
                elif self.position[1] + 20 > (game.PADDLE2_Y + game.PADDLESIZE/2):  # left paddle, bottom tip
                    self.angle = 180 - self.angle + 20
                else:  # left paddle center
                    self.angle = 180 - self.angle
                sounds.ping_pong_8bit_beeep.play(0, 300)
            else:
                if self.position[0] > WIDTH + 20: # ball is out of screen on the right
                    sounds.ping_pong_8bit_peeeeeep.play(0, 300)
                    game.playingball = False
                    game.scoreP1 += 1

# ---------------------- GAME CLASS ---------------------
class GameClass:
    def __init__(self):
        self.time = 0
        self.scoreP1 = 0
        self.scoreP2 = 0
        self.playingball = False
        self.PADDLESIZE = 150
        self.PADDLESPEED = 20
        self.PADDLE1_Y = HEIGHT/2
        self.PADDLE1 = Rect((50, self.PADDLE1_Y - self.PADDLESIZE/2), (20, self.PADDLESIZE))
        self.PADDLE2_Y = HEIGHT/2
        self.PADDLE2 = Rect((WIDTH - 70, self.PADDLE2_Y - self.PADDLESIZE/2), (20, self.PADDLESIZE))
        self.ball = BallClass()
    
    def nextball(self):
        self.PADDLE1_Y = HEIGHT/2
        self.PADDLE1 = Rect((50, self.PADDLE1_Y - self.PADDLESIZE/2), (20, self.PADDLESIZE))
        self.PADDLE2_Y = HEIGHT/2
        self.PADDLE2 = Rect((WIDTH - 70, self.PADDLE2_Y - self.PADDLESIZE/2), (20, self.PADDLESIZE))
        self.playingball = True
        self.ball = BallClass()
   
game = GameClass()


# ---------------------- DRAW ---------------------
def draw():
    screen.clear()
    screen.draw.filled_rect(game.PADDLE1, "white")
    screen.draw.filled_rect(game.PADDLE2, "white")
    screen.draw.line((WIDTH/2, 50), (WIDTH/2, HEIGHT - 50), "white")
    screen.draw.filled_rect(game.ball.rect, "white")
    screen.draw.text(str(game.scoreP1), (WIDTH/4, 60), color="white", fontsize= 120)
    screen.draw.text(str(game.scoreP2), (WIDTH - WIDTH/4, 60), color="white", fontsize= 120)    

    if not game.playingball:
        screen.draw.text("PRESS SPACE TO CONTINUE, R TO RESTART \n          FOR CONTROL USE Q&A and O&K", (WIDTH/2 - 150, HEIGHT / 2), background="black", color="white")

# ---------------------- UPDATE ---------------------
def update():

    if keyboard.r:
        game.__init__()
    
    if game.playingball:
        game.ball.update_ball()
        if keyboard.q and (game.PADDLE1_Y - game.PADDLESIZE/2) > 0:
            game.PADDLE1_Y -= game.PADDLESPEED
            game.PADDLE1 = Rect((50, game.PADDLE1_Y - game.PADDLESIZE/2), (20, game.PADDLESIZE))
        if keyboard.a and (game.PADDLE1_Y + game.PADDLESIZE/2) < HEIGHT:
            game.PADDLE1_Y += game.PADDLESPEED
            game.PADDLE1 = Rect((50, game.PADDLE1_Y - game.PADDLESIZE/2), (20, game.PADDLESIZE))
        if keyboard.o and (game.PADDLE2_Y - game.PADDLESIZE/2) > 0:
            game.PADDLE2_Y -= game.PADDLESPEED
            game.PADDLE2 = Rect((WIDTH - 70, game.PADDLE2_Y - game.PADDLESIZE/2), (20, game.PADDLESIZE))
        if keyboard.k and (game.PADDLE2_Y + game.PADDLESIZE/2) < HEIGHT:
            game.PADDLE2_Y += game.PADDLESPEED
            game.PADDLE2 = Rect((WIDTH - 70, game.PADDLE2_Y - game.PADDLESIZE/2), (20, game.PADDLESIZE))
    else:
        if keyboard.SPACE:
            game.nextball()


# pgz.run()
#     print(game.playingball)
#     print(game.ball.position[0])
