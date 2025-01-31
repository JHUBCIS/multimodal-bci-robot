import serial
import time
from upd_processing_pipeline import BCIProcessingPipeline
import socket
import pyautogui
from pynput.keyboard import Controller

# HOST = 'localhost'
# PORT = 5555

if __name__ == '__main__':
    
    pipeline = BCIProcessingPipeline(buffer_size=10)
    port_id = "COM12"
    
    keyboard = Controller()
    press_time = 0

    print('Running. Press CTRL-C to exit.')
    
    cur_state = (0, 0)

    with serial.Serial(port_id, 115200, timeout=1) as arduino:

        time.sleep(0.1)  # Wait for serial to open

        if arduino.isOpen():
            print(f"{arduino.port} connected!")

            cycles = 0
            acc = 0

            while True:
                # Wait for data from Arduino
                while arduino.inWaiting() == 0:
                    pass
                s_line = arduino.readline()

                try:
                    Emg_bp0, Emg_bp1 = [
                        float(x) for x in s_line.decode('utf-8').strip().split(' ')
                    ]
                except Exception as e:
                    print('Error decoding message', e)
                    continue

                cycles += 1
                acc += Emg_bp1
                if cycles % 100 == 0:
                   print(f"Avg EMG: {acc/100}")
                   acc = 0

                # Run pipeline prediction
                output = pipeline.predict(Emg_bp0, Emg_bp1)


                # Suppose output is [1,0] for CHEEK, [0,1] for NECK
                w
                    # Send command to turtle
                # elif output[1] == 0:
                #     if cur_state[1] == 1:
                        # pyautogui.keyUp('d')

                cur_state = output

# import serial
# from time import sleep
# from upd_processing_pipeline import BCIProcessingPipeline
# import socket
# from pynput.keyboard import Key, Controller

# # HOST = 'localhost'
# # PORT = 5555

# if __name__ == '__main__':
    
#     pipeline = BCIProcessingPipeline(buffer_size=10)
#     port_id = "COM12"
    
#     print('Running. Press CTRL-C to exit.')
#     keyboard = Controller()

#     with serial.Serial(port_id, 115200, timeout=1) as arduino:

#         sleep(0.1)  # Wait for serial to open

#         if arduino.isOpen():
#             print(f"{arduino.port} connected!")

#             cycles = 0
#             acc = 0

#             while True:
#                 # Wait for data from Arduino
#                 while arduino.inWaiting() == 0:
#                     pass
#                 s_line = arduino.readline()

#                 try:
#                     Emg_bp0, Emg_bp1 = [
#                         float(x) for x in s_line.decode('utf-8').strip().split(' ')
#                     ]
#                 except Exception as e:
#                     print('Error decoding message', e)
#                     continue

#                 cycles += 1
#                 acc += Emg_bp1
#                 if cycles % 100 == 0:
#                    print(f"Avg EMG: {acc/100}")
#                    acc = 0

#                 # Run pipeline prediction
#                 output = pipeline.predict(Emg_bp0, Emg_bp1)

#                 # Suppose output is [1,0] for CHEEK, [0,1] for NECK
#                 if output[0] == 1:
#                     print("Cheek :O")
#                     keyboard.press('a')
#                     # Send command to turtle
#                 elif output[0] == 0:
#                     keyboard.release('a')

#                 if output[1] == 1:
#                     keyboard.press('d')
#                     print("Neck B)")
#                     # Send command to turtle
#                 elif output[1] == 1:
#                     keyboard.release('d')