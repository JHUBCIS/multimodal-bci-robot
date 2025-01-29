import turtle
from typing import Dict

class TurtleController:
    MOVE_DISTANCE = 10
    TURN_ANGLE = 10
    UPDATE_INTERVAL = 50  

    def __init__(self):
        self.turtle = turtle.Turtle()
        self.turtle.speed(0) 
        self.turtle.shapesize(2, 2)
        self.screen = turtle.Screen()
        self.screen.setup(600, 600)
        
        # Dot writing turtle init
        self.dot = turtle.Turtle()
        self.dot.hideturtle()
        self.dot.penup()
        self.dot.color('red')
        
        # Score display turtle init
        self.score_display = turtle.Turtle()
        self.score_display.hideturtle()
        self.score_display.penup()
        self.score_display.goto(0, 250)
        self.score = 0
        
        self.key_states: Dict[str, bool] = {
            'w': False, 
            's': False,  
            'a': False, 
            'd': False,
        }
        
        self.setup_controls()
        self.screen.listen()
        self.update_score_display()
        self.create_new_dot()
        
    def setup_controls(self):
        for key in self.key_states:
            # cheeky lambda :)
            self.screen.onkeypress(lambda k=key: self.handle_keychange(k, True), key)
            self.screen.onkeyrelease(lambda k=key: self.handle_keychange(k, False), key)

    def handle_keychange(self, key: str, state: bool):
        self.key_states[key] = state

    def create_new_dot(self):
        import random
        x = random.randint(-250, 250)
        y = random.randint(-250, 250)
        self.dot.clear()
        self.dot.goto(x, y)
        self.dot.dot(20)

    def check_collision(self):
        if self.turtle.distance(self.dot) < 30:
            self.score += 1 
            self.update_score_display()
            self.create_new_dot()

    def check_out_of_bounds(self):
        # Wrap around if turtle goes beyond ±290 in either x or y
        x, y = self.turtle.position()
        if x > 290:
            x = 290
        elif x < -290:
            x = -290
        if y > 290:
            y = 290
        elif y < -290:
            y = -290

        self.turtle.goto(x, y)

    def update(self):

        if self.key_states['w']:
            self.turtle.forward(self.MOVE_DISTANCE)
        if self.key_states['s']:
            self.turtle.backward(self.MOVE_DISTANCE)
        if self.key_states['a']:
            self.turtle.left(self.TURN_ANGLE)
        if self.key_states['d']:
            self.turtle.right(self.TURN_ANGLE)

        self.check_collision()
        self.check_out_of_bounds()
        self.screen.ontimer(self.update, self.UPDATE_INTERVAL)

    def run(self):
        self.update()
        turtle.mainloop()

    def update_score_display(self):
        self.score_display.clear()
        self.score_display.write(f"Score: {self.score}", align="center", font=("Arial", 16, "normal"))

if __name__ == "__main__":
    controller = TurtleController()
    controller.run()
