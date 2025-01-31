import turtle
# import socket
# import threading
# import queue

class TurtleController:
    UPDATE_INTERVAL = 50  # ms, frequency of update calls
    FORWARD_SPEED = 5     # in pixels
    TURN_SPEED = 3        # in degrees

    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(width=800, height=600)
        self.screen.title("Turtle Exp. 1, 2 DOF")

        self.turtle = turtle.Turtle()
        self.turtle.shape("turtle")
        self.turtle.color("blue")
        self.turtle.penup()
        self.turtle.speed(0)

        # For our 800x600 screen, the coordinate system is roughly +/- 400 in X and +/- 300 in Y
        self.MIN_X, self.MAX_X = -380, 380
        self.MIN_Y, self.MAX_Y = -280, 280

        # States for toggling movement
        self.moving_forward = False
        self.moving_backward = False
        self.moving_left = False
        self.moving_right = False
        # self.rotating_left = False

        # Dots to collect
        self.dot = turtle.Turtle()
        self.dot.shape("circle")
        self.dot.color("red")
        self.dot.penup()
        self.dot.goto(-340, 240)
        self.dot.shapesize(1,1)

        # Only using 3 corners so we can have the turtle do a diagonal
        self.corners = [(-340,240),(340,240),(340,-240)]
        self.corners_index = 0
        
        # Comment out for reading EMG signals
        self.screen.listen() #listen for keyboarssd events
        self.screen.onkey(self.toggle_forward, "w")
        self.screen.onkey(self.toggle_backward, "s")
        self.screen.onkey(self.toggle_left, "a")
        self.screen.onkey(self.toggle_right, "d")

        # FOR EMG INPUT -------------------------------------------------
        # A thread-safe queue to store incoming commands
        #self.command_queue = queue.Queue()

        # Start a background thread that listens for incoming connections
        
        # self.server_thread = threading.Thread(
        #     target=self.start_server, 
        #     args=(host, port), 
        #     daemon=True
        # )
        # self.server_thread.start()
        
        
    # def start_server(self, host, port):
    #     """
    #     Opens a TCP server socket and listens for commands from the pipeline.
    #     """
    #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #         s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #         s.bind((host, port))
    #         s.listen(1)
    #         print(f"[TurtleController] Listening on {host}:{port} ...")

    #         while True:
    #             conn, addr = s.accept()
    #             print(f"[TurtleController] Connected by {addr}")
    #             with conn:
    #                 while True:
    #                     data = conn.recv(1024)
    #                     if not data:
    #                         break
    #                     # data might contain multiple commands separated by newline
    #                     commands = data.decode('utf-8').strip().split('\n')
    #                     for cmd in commands:
    #                         if cmd:
    #                             self.command_queue.put(cmd)
    #                             print(f"[TurtleController] Received command: {cmd}")

    # def handle_command(self, cmd):
    #     """
    #     Translate a command string into toggles for continuous movement.
    #     """
    #     cmd_upper = cmd.upper().strip()

    #     if cmd_upper == "CHEEK":
    #         # Toggle forward movement on/off
    #         self.moving_forward = not self.moving_forward
    #         print(f"[TurtleController] Toggled moving_forward = {self.moving_forward}")s
    #     elif cmd_upper == "NECK":
    #         # Toggle left rotation on/off
    #         self.rotating_left = not self.rotating_left
    #         print(f"[TurtleController] Toggled rotating_left = {self.rotating_left}")

    #     # Add any other commands you might need...
    #     # elif cmd_upper == "WHATEVER":
    #     #     ...
    # END OF EMG INPUT FUNCTIONS ----------------------------------------

    def toggle_forward(self):
        self.moving_forward = not self.moving_forward

    def toggle_backward(self):
        self.moving_backward = not self.moving_backward

    def toggle_left(self):
        self.moving_left = not self.moving_left

    def toggle_right(self):
        self.moving_right = not self.moving_right

    def toggle_rotation(self):
        self.rotating_left = not self.rotating_left
   
    def toggle_turn_left(self):
        self.turtle.left(90)

    def toggle_turn_right(self):
        self.turtle.right(90)

    
    def update(self):
        """
        Periodically called by the turtle's event loop. 
        Process any commands from the command queue and move/turn the turtle if toggled.
        Then, clamp the position if it goes outside the boundaries.
        """
        # FOR EMG INPUT
        # 1) Process all commands in the queue
        #while not self.command_queue.empty():
            #cmd = self.command_queue.get_nowait()
            #self.handle_command(cmd)

        # 2) Move or turn if toggled
        if self.moving_forward:
            self.turtle.forward(self.FORWARD_SPEED)
        elif self.moving_backward:
            self.turtle.backward(self.FORWARD_SPEED)
        elif self.moving_left:
            self.turtle.left(self.FORWARD_SPEED)
        elif self.moving_right:
            self.turtle.right(self.FORWARD_SPEED)

        # if self.rotating_left:
        #     self.turtle.left(self.TURN_SPEED)

        # 3) Enforce boundariess
        self.check_boundaries()

        # 4) Schedule the next updates
        self.screen.ontimer(self.update, self.UPDATE_INTERVAL)

        self.check_collision()

    def place_dot(self):
        self.dot.goto(self.corners[self.corners_index])

    def check_collision(self):
        turtle_pos = self.turtle.position()
        dot_pos = self.dot.position()

        if self.turtle.distance(dot_pos) < 20:
            self.corners_index = (self.corners_index + 1) % len(self.corners)
            self.place_dot()

    def check_boundaries(self):
        """
        If the turtle goes outside the defined boundaries,
        clamp its (x, y) position to keep it in-bounds.
        """
        x, y = self.turtle.position()

        # Clamp X
        if x < self.MIN_X:
            self.turtle.setx(self.MIN_X)
        elif x > self.MAX_X:
            self.turtle.setx(self.MAX_X)

        # Clamp Y
        if y < self.MIN_Y:
            self.turtle.sety(self.MIN_Y)
        elif y > self.MAX_Y:
            self.turtle.sety(self.MAX_Y)

    def run(self):
        """Start the periodic update and turtle mainloop."""
        # Kick off the first scheduled update
        self.update()
        # Enter the turtle main loop (blocking)
        turtle.mainloop()

if __name__ == "__main__":
    controller = TurtleController() #host='localhost', port=5555  *ADD FOR EMG INPUT
    controller.run()