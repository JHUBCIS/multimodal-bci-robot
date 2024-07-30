from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate
from pandas import read_csv
import numpy as np
import joblib

def create_overlapping_sliding_windows(data, window_size, overlap):
    windows = []
    for i in range(0, len(data) - window_size + 1, overlap):
        windows.append(data[i:i+window_size, :])
    return np.array(windows)

# Generate some random data for classification
data = read_csv("data/Cheek_Neck_EMG.csv")

# Gets the badnpassed EMG data
emg_data = data.iloc[:, 6:8]
emg_data = emg_data.to_numpy()

button_data = data.iloc[:, 2:4]
button_data = button_data.to_numpy()

# Create overlapping sliding windows of 100 timesteps with 40 overlap
windowed_emg_data = create_overlapping_sliding_windows(emg_data, 100, 40)
windowed_button_labels = create_overlapping_sliding_windows(button_data, 100, 40)

X = np.sqrt(np.mean(np.square(windowed_emg_data), axis=1))
y = np.max(windowed_button_labels, axis=1)

RMS_EMG_0 = X[:,0].reshape(-1, 1)
button_0 = y[:, 0]

RMS_EMG_1 = X[:,1].reshape(-1, 1)
button_1 = y[:, 1]

cv_results_0 = cross_validate(LogisticRegression(), RMS_EMG_0, button_0, cv=5, scoring='accuracy', return_estimator=True)
cv_results_1 = cross_validate(LogisticRegression(), RMS_EMG_1, button_1, cv=5, scoring='accuracy', return_estimator=True)

emg_0_model = cv_results_0['estimator'][cv_results_0['test_score'].argmax()]
emg_1_model = cv_results_1['estimator'][cv_results_1['test_score'].argmax()]

joblib.dump(emg_0_model, 'saved_models/emg_0_model.pkl')
joblib.dump(emg_1_model, 'saved_models/emg_1_model.pkl')


# <--- For Debugging if Zach Rebases --->
#import os
#current_working_directory = os.getcwd()
#print(f"Current Working Directory: {current_working_directory}")