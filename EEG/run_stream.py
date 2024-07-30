import os
import numpy as np
import pandas as pd

from eegnb import generate_save_fn
from eegnb.devices.eeg import EEG
# from eegnb.devices.eeg_rt_plot_mpl import EEGRealTimePlotMPL

board_name = "unicorn"
experiment = "stream test"
subject_id = 0
session_nb = 0

# Create save file name
save_fn = generate_save_fn(board_name, experiment, subject_id, session_nb)

# define the name for the board you qare using and call the EEG object
eeg = EEG(device='unicorn')

# start the stream
# eeg.stream(save_fn)
eeg.stream_plot(save_fn,buffer_time=15, bp_fc_high = 60, bp_fc_low = 1, n_fc = 60)


