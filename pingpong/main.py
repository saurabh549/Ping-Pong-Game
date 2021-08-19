from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty,ReferenceListProperty,ObjectProperty,StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint
Window.clearcolor=(0,61/255,0,1)
class PongPaddle(Widget):
    score= NumericProperty(0)
    def bounce_ball(self,ball):
        if self.collide_widget(ball):
            ball.velocity_x*=-1.2
class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    player1=ObjectProperty(None)
    player2=ObjectProperty(None)
    velocity = ReferenceListProperty(velocity_x,velocity_y)
    def move(self):
        self.pos = Vector(*self.velocity)+self.pos
class PongGame(Widget):
    ball=ObjectProperty(None)
    txt = StringProperty("")
    def server_ball(self):
        self.ball.velocity=Vector(4,0).rotate(randint(0,360))
    def update(self,dt):
        self.ball.move()
        if (self.ball.y<0) or (self.ball.y>self.height-50):
            self.ball.velocity_y *= -1
        if (self.ball.x<0):
            self.ball.center=self.parent.center
            self.server_ball()
            self.player1.score+=1
        if (self.ball.x>self.width-50):
            self.ball.center = self.parent.center
            self.server_ball()
            self.player2.score += 1
        if(self.player1.score==10):
            self.ball.velocity = Vector(0, 0)
            self.txt="Player 2 Wins the Match"
            return False
        if (self.player2.score == 10):
            self.ball.velocity = Vector(0, 0)
            self.txt = "Player 1 Wins the Match"
            return False
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
    def on_touch_move(self, touch):
        if touch.x<self.width*1/4:
            self.player1.center_y=touch.y
        if touch.x>self.width*3/4:
            self.player2.center_y=touch.y
class PongApp(App):
    def build(self):
        game = PongGame()
        game.server_ball()
        Clock.schedule_interval(game.update,1.0/90.0)
        return game
PongApp().run()