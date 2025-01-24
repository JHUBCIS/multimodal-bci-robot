from pylsl import StreamInlet, resolve_stream
from cca import CCAClassifier
import multiprocessing
import time
import random
import pandas as pd
import numpy as np

def acceptNewValue(elem : list):
   global global_values

   
   if counter < (num_samples_per):
      return

   global_values = np.concatenate((elem, global_values[0:-batch_size]), axis=0)

   val = classifier.classify_cca(global_values)
   print(np.argmax(val))

  
# initialize the streaming layer
finished = False
streams = resolve_stream()
inlet = StreamInlet(streams[0])

# initialize the colomns of your data and your dictionary to capture the data.
columns=['Time','FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8','AccX','AccY','AccZ',
'Gyro1','Gyro2','Gyro3', 'Battery','Counter','Validation']
data_dict = dict((k, []) for k in columns)

prev_timestamp = 0

total_time = 0
counter = 1

SAMPLE_RATE = 250

WINDOW_SIZE = 7 # seconds

num_samples_per = SAMPLE_RATE * WINDOW_SIZE

classifier = CCAClassifier();

batch_size = 750
batch = []
global_values = np.zeros((num_samples_per,8))

cca_classification_on = True

global_index = 0

time_recording = 1

inf_run = True

file = -1
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

      batch.append(np.array(data[0:8]))

      if (counter) % (batch_size) == 0:

         acceptNewValue(batch.copy())


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