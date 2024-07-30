#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name

import serial
# import threading

from time import sleep
from upd_processing_pipeline import BCIProcessingPipeline
from emg_mqtt import connect_mqtt, publish
# import keyboard
from pynput import keyboard

# Re-write the code to take advantage of parallel processing
# Use joblib to load the files

is_space_pressed = False

def on_press(key):
    global is_space_pressed
    if key == keyboard.Key.space:
        is_space_pressed = True

def on_release(key):
    global is_space_pressed
    if key == keyboard.Key.space:
        is_space_pressed = False

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

if __name__ == '__main__':
    
    pipeline = BCIProcessingPipeline(buffer_size=10)
    client = connect_mqtt()
    port_id = "/dev/ttyACM0"
    
    print('Running. Press CTRL-C to exit.')
    with serial.Serial(port_id, 115200, timeout=1) as arduino:

        sleep(0.1) # wait for serial to open

        if arduino.isOpen():
            print("{} connected!".format(arduino.port))

            cycles = 0
            acc = 0

            while True:

                sleep(0.0001) # wait for arduino to answer

                while arduino.inWaiting()==0: pass
                if  arduino.inWaiting()>0: 
                    # print(str(arduino.readline()))
                    s = arduino.readline()
                    # print(s)
                    try:
                        Emg_bp0, Emg_bp1 = [float(x) for x in s.decode('utf-8').strip().split(' ')]
                        cycles += 1
                        acc += Emg_bp1
                    except:
                        print('Error decoding message')
                        continue

                # prints average EMG activity every 100 cycles
                    if cycles % 100 == 0:
                        print(acc/100)
                        acc = 0

                    output = pipeline.predict(Emg_bp0, Emg_bp1)

                    if output[0] == 1:
                        print('Cheek :O')
                        if is_space_pressed:
                            publish(client, '1')
                    if output[1] == 1:
                        print('Neck B)')
                        if is_space_pressed:
                            publish(client, '2')

                    # if output[0] == 1:
                    #     print('Cheek :O')
                    #     # if keyboard.is_pressed('space'):
                    #     publish(client, '1')
                    # if output[1] == 1:
                    #     print('Neck B)')
                    #     # if keyboard.is_pressed('space'):
                    #     publish(client, '2')
