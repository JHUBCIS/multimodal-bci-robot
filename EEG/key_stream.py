import keyboard
import socket 
def unicorn_on_key_event(event):
    if event.event_type == keyboard.KEY_DOWN:
        sendBytes = ''
        if event.name == 'a':
            # Send trigger
            sendBytes = b"1"
        elif event.name == 'd':
            # Send trigger
            sendBytes = b"2"

        #add your keys/triggers here

        if len(sendBytes)>0:
            print('Key: ' + event.name + ' Sending: ' + str(sendBytes))
            try:
                socket.sendto(sendBytes, endPoint)
                print(f"Sent {sendBytes} to {endPoint}")
            except Exception as e:
             print(f"Failed to send data: {e}")


socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
endPoint = ("127.0.0.1", 800)

keyboard.on_press(unicorn_on_key_event)
keyboard.wait('esc')