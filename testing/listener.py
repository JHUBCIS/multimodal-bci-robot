import keyboard

def on_u_press(event):
    keyboard.write('w')

keyboard.on_press_key('u', on_u_press)
keyboard.wait()  # Keep the program running