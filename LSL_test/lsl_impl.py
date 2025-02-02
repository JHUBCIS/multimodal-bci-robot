from pylsl import StreamInlet, resolve_stream
from cca import CCAClassifier
import multiprocessing
import time
import random
import pandas as pd
import numpy as np
import socket
import csv
from scipy.stats import norm
from pynput.keyboard import Controller
from playsound import playsound

# for playing note.mp3 file

def acceptNewValue(elem : list):
   global global_values
   global state_s

   
   if counter < (num_samples_per):
      return

   global_values = np.concatenate((elem, global_values[0:-batch_size]), axis=0)

   val = classifier.classify_cca(global_values)
   if state_s<4:
      print(np.argmax(val)," ", val)
   return val

SEGREGATED_COLLECTION = True
  
# initialize the streaming layer
finished = False
streams = resolve_stream()
inlet = StreamInlet(streams[0])

# initialize the colomns of your data and your dictionary to capture the data.
columns=['Time','FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8','AccX','AccY','AccZ',
'Gyro1','Gyro2','Gyro3', 'Battery','Counter','Validation']
data_dict = dict((k, []) for k in columns)

prev_timestamp = 0

keyboard = Controller()
press_time = 0

total_time = 0
counter = 1

SAMPLE_RATE = 250

WINDOW_SIZE = 7 # seconds

num_samples_per = SAMPLE_RATE * WINDOW_SIZE

classifier = CCAClassifier();

batch_size = 127 #750
batch = []
global_values = np.zeros((num_samples_per,8))

cca_classification_on = True

global_index = 0

time_recording = 1

inf_run = True

calibration = {"blank": [], "slow": [], "fast": []}
state_s = 0

super_batch = []
logit_super = []

file = -1

# UDP_IP = "127.0.0.1"
# UDP_PORT = 800

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind(UDP_IP, UDP_PORT)

# calibration_data = {'2': [],
#                     '3': [],
#                     '4': []}

first = True
# if inf_run:
   # file = open("inf_run.csv", "w")
   # file.write(",".join(columns) + ", \n")
   # file.close()

   #file = open("inf_run.csv", "a")


while not finished:
   # get the streamed data. Columns of sample are equal to the columns variable, only the first element being timestamp
   # concatenate timestamp and data in 1 list
   data, timestamp = inlet.pull_sample()
   all_data = [timestamp] + data
   
   #print("Latency: ", (timestamp-prev_timestamp), " Intended: ", em)
   prev_timestamp = timestamp

   # calibration_bytes, addr = sock.recvfrom(1024)
   # calibration_code = calibration_bytes.decode()

   # print(calibration_code)

   # updating data dictionary with newly transmitted samples   
   i = 0

   if not inf_run:

      for key in list(data_dict.keys()):
         data_dict[key].append(all_data[i])
         # add in a index timestamp

         i = i + 1
      
   #else:
      #file.write(",".join([str(x) for x in all_data]) + "\n")
      

   # adding a global index for the data
   #data_dict.append(global_index)
   #global_index += 1
   
   # data is collected at 250 Hz. Let's stop data collection after 60 seconds. Meaning we stop when we collected 250*60 samples.
   time_stamp_malcolm = time.perf_counter()

   if (len(data_dict['Time']) >= 250 * time_recording) and not inf_run:
      finished = True

   
   if cca_classification_on:

      batch.insert(0,np.array(data[0:8]))

      if (counter) % (batch_size) == 0:
         logits = acceptNewValue(batch.copy())
         if logits != None and state_s < 4:
            super_batch.append(logits[0]-logits[1])
            logit_super.append(logits)

            # if calibration_code == 2:
            #    calibration_data['2'].append(logits[0]-logits[1])
            # elif calibration_code == 3:
            #    calibration_data['3'].append(logits[0]-logits[1])
            # elif calibration_code == 4:
            #    calibration_data['4'].append(logits[0]-logits[1])
            # else:
            #    pass

         if first:
            first = False

         if SEGREGATED_COLLECTION and state_s < 4:

            if (counter % (batch_size * 70)) == 0:
               super_batch = []
               logit_super = []
               print("----------------------------unpausing--------------------------")

            if (counter % (batch_size * 70)) == (batch_size * 50):
               # slow_hz, fast_hz = zip(*super_batch)
               print(f"stdev: {np.std(super_batch)},  mean: {np.mean(super_batch)} range: {max(super_batch) - min(super_batch)}, max: {max(super_batch)}, min: {min(super_batch)}")
               if (state_s == 1):
                  calibration["blank"] = super_batch
               elif (state_s == 2):
                  calibration["slow"] = super_batch
               elif (state_s == 3):
                  calibration["fast"] = super_batch
                  # write baysian calc

                  blank_params = norm.fit(calibration["blank"])
                  slow_params = norm.fit(calibration["slow"])
                  fast_params = norm.fit(calibration["fast"])
                  print("------------------------youre at the end lol ---------------------")



               state_s += 1

               with open(f"data_{counter/batch_size}.csv", 'w', newline='') as File:
                  csvwriter = csv.writer(File)

                  csvwriter.writerows(logit_super)   
               # print(f"The stdev of slow: {np.std(slow_hz)}, the mean is {np.mean(slow_hz)} and the range is {max(slow_hz) - min(slow_hz)}, with the max being {max(slow_hz)}, and the min being {min(slow_hz)}")

               print("-------------------get ready to switch--------------------------")
         else:
            sample = logits[0]-logits[1]
            p_blank = norm.pdf(sample, loc=blank_params[0], scale=blank_params[1])
            p_slow = norm.pdf(sample, loc=slow_params[0], scale=slow_params[1])
            p_fast = norm.pdf(sample, loc=fast_params[0], scale=fast_params[1])

            # pred = np.argmax([p_blank, p_slow, p_fast])
            
            # if sample > slow_params[0]:
            if sample > blank_params[0] + 2*blank_params[1]:
               pred = 1
            # elif sample < fast_params[0]:
            elif sample < blank_params[0] - 2*blank_params[1]:
               pred = 2
            else:
               pred = 0

            print(pred)

            if pred == 1 and (time.time() - press_time) > 2:
               print('Slow...')
               press_time = time.time()
               keyboard.press('w')
               keyboard.release('w')


            if pred == 2 and (time.time() - press_time) > 2:
               print('Fast!!!')
               press_time = time.time()
               keyboard.press('s')
               keyboard.release('s')

         batch = []


      #else:

         #dict_values = data_dict.values()

         #values = [item for item in data_dict.items()]
         #last_values = [(key, value[-1]) for key, value in values]
         #batch.append(np.array([x[1] for x in last_values]))

         # Isomorphic Code:
         # last_values = [value[-1] for value in data_dict.values]
         # batch.append(np.array(last_values[1:9]))

         # Zachs code
         #batch.append(np.array(data[0:8]))
         #batch.append(np.array(list(data_dict.values())[1:9]))

   
   end_time = time.perf_counter()
   counter += 1
   total_time += end_time - time_stamp_malcolm




print("Average Elapsed: " , total_time/counter)

# lastly, we can save our data to a CSV format.
data_df = pd.DataFrame.from_dict(data_dict)
data_df.to_csv('EEGdataaa.csv', index = False)