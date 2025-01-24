import turtle
from typing import Dict

class TurtleController:
    MOVE_DISTANCE = 10
    TURN_ANGLE = 10
    UPDATE_INTERVAL = 50  

    def __init__(self):
        self.turtle = turtle.Turtle()
        self.turtle.speed(0) 
        self.turtle.shapesize(2, 2)  # make the turtle bigger
        self.screen = turtle.Screen()
        
        # Garbage and I hate it
        self.key_states: Dict[str, bool] = {
            'w': False, 
            's': False,  
            'a': False, 
            'd': False,
        }
        
        self.setup_controls()
        self.screen.listen()
        
    def setup_controls(self):
        for key in self.key_states:
            # cheeky lambda :)
            self.screen.onkeypress(lambda k=key: self.handle_keychange(k, True), key)
            self.screen.onkeyrelease(lambda k=key: self.handle_keychange(k, False), key)

    def handle_keychange(self, key: str, state: bool):
        self.key_states[key] = state

    def update(self):
        # oooga booga - i should use a switch statement - but i dont want to 
        if self.key_states['w']:
            self.turtle.forward(self.MOVE_DISTANCE)
        if self.key_states['s']:
            self.turtle.backward(self.MOVE_DISTANCE)
        if self.key_states['a']:
            self.turtle.left(self.TURN_ANGLE)
        if self.key_states['d']:
            self.turtle.right(self.TURN_ANGLE)
            
        self.screen.ontimer(self.update, self.UPDATE_INTERVAL)

    def run(self):
        # start game
        self.update()
        turtle.mainloop()

if __name__ == "__main__":
    controller = TurtleController()
    controller.run()
