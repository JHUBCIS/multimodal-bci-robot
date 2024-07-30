"""
ssvep run experiment
===============================

This example demonstrates the initiation of an EEG stream with eeg-expy, and how to run 
an experiment. 


"""

###################################################################################################  
# Setup
# ---------------------  
#  
# Imports
# from eegnb import generate_save_fn
# from eegnb.devices.eeg import EEG
from eegnb.experiments.visual_ssvep.ssvep_select_unicorn import VisualSSVEP_select_unicorn
from eegnb.experiments.visual_ssvep.ssvep_select_unicorn_emg_ortho import VisualSSVEP_select_unicorn_emg_ortho
# from eegnb.experiments.visual_ssvep.ssvep import VisualSSVEP

# Define some variables
# board_name = "unicorn" # board name
# experiment_name = "ssvep_select" # experiment name
# subject_id = 0 # test subject id
# session_nb = 0 # session number
record_duration = 500  # recording duration in seconds

# generate save path
# save_fn = generate_save_fn(board_name, experiment_name, subject_id, session_nb)

# create device object
#eeg_device = EEG(device=board_name)   

# Experiment type
# experiment = VisualSSVEP(duration=record_duration, eeg=eeg_device, save_fn=save_fn)
'''for more details on which frequencies to select, see https://www.nature.com/articles/s41597-023-02841-5'''
# experiment = VisualSSVEP_select_unicorn(duration=record_duration, freq1=9.75, freq2=14.25, IP="127.0.0.1", Port=800) #note that most laptops only support up to 60 Hz. don't go above that
experiment = VisualSSVEP_select_unicorn_emg_ortho(duration=record_duration, freq1=9.75, freq2=14.25, IP="127.0.0.1", Port=1000) #note that most laptops only support up to 60 Hz. don't go above that

###################################################################################################  
# Run experiment
# ---------------------  
#
experiment.run()

