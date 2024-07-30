
from numpy import zeros, mean, square, asarray
from math import sqrt

import joblib


class BCIProcessingPipeline:


    # Correspond one and two to check / neck
    # Use job lib to load the files


    def __init__(self, buffer_size = 10, file_one = '../saved_models/emg_0_model.pkl', file_two = '../saved_models/emg_1_model.pkl'):

        # intialize the buffer size and the buffer
        self.buffer_size = buffer_size
        self.buffer_one = zeros(buffer_size)
        self.buffer_two = zeros(buffer_size)

        self.buffer_pointer = 0

        self.buffer_sum_one = 0
        self.buffer_sum_two = 0

        # load the two models from pkl file
        self.loaded_model_one = joblib.load(file_one)
        self.loaded_model_two = joblib.load(file_two)

    def update(self, new_data_one, new_data_two):

        # Updates the values in the buffer and the buffer sum

        # # Edit the buffer one sum
        # self.buffer_sum_one -= (self.buffer_one[self.buffer_pointer])**2
        # self.buffer_sum_one += (new_data_one)**2

        # # Edit the buffer two sum   
        # self.buffer_sum_two -= (self.buffer_two[self.buffer_pointer])**2
        # self.buffer_sum_two += (new_data_two)**2

        # Edit buffer
        self.buffer_one[self.buffer_pointer] = new_data_one
        self.buffer_two[self.buffer_pointer] = new_data_two 

        self.buffer_pointer = (self.buffer_pointer + 1) % self.buffer_size

    def process_data(self):

        # Returns the RMS of the buffer
        return sqrt(mean(square(self.buffer_one))), sqrt(mean(square(self.buffer_two)))
    
    def reset(self):

        # Resets the buffer to 0
        self.buffer = zeros(self.buffer_size)
        self.buffer_pointer = 0
        self.buffer_sum = 0

    def predict(self, new_data_one, new_data_two):

        # Updates the buffer and returns the RMS of the buffer
        self.update(new_data_one, new_data_two)
        rms_one, rms_two = self.process_data()

        return self.loaded_model_one.predict(asarray(rms_one).reshape(-1,1))[0], self.loaded_model_two.predict(asarray(rms_two).reshape(-1,1))[0]
