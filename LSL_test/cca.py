from sklearn.cross_decomposition import CCA
import pandas as pd
import numpy as np
import mne


columns=['FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8']

file_name = "inbf_run.csv"

big_boy = []
class CCAClassifier:

    def __init__(self) -> None:

        mne.set_log_level('WARNING')
        # hyperparameters from the CCA notebook
        self.event_freq = [9.75, 14.25]
        self.tmax = 3
        self.fs = 250

        file = open(file_name, "w")
        file.write(",".join(columns) + ", \n")
        file.close()

        self.file = open(file_name, "a")

        self.cca_classifier = CCAAnalysis(freqs=self.event_freq, win_len=self.tmax, s_rate=self.fs, n_harmonics=2)


    def classify_cca(self, twod_array_to_classify : np.array) -> int:
        # Lambda: Apply bandpass filter

        twod_array_to_classify = twod_array_to_classify.T

        band_pass_filtered = mne.filter.filter_data(twod_array_to_classify, 250, 0.5, 50)
        #band_pass_filtered = [mne.filter.filter_data(x, 250, 0.5, 50) for x in twod_array_to_classify]

        # Lambda: Apply notch filter
        notch_filtered = mne.filter.notch_filter(band_pass_filtered, 250, (60))
        #notch_filtered = [mne.filter.notch_filter(x, 250, (60)) for x in band_pass_filtered]

        notch_filtered = notch_filtered.T

        #print(notch_filtered.shape)
        notch_filtered = np.array(notch_filtered[:int(250 * (self.tmax))])
        #print(notch_filtered.shape)

        #for channel in notch_filtered:
        #    if len(channel) < int(self.fs*self.tmax):
        #        continue

        # print(twod_array_to_classify.shape)

        # twod_array_to_classify = np.append(twod_array_to_classify, [twod_array_to_classify[-1]], axis=0)

        # print(twod_array_to_classify.shape)
        
        score = self.cca_classifier.apply_cca(np.array(notch_filtered))

        for val in notch_filtered:
            self.file.write(",".join([str(x) for x in val]) + "\n")

        return score

class CCAAnalysis:
    """Canonical Correlation Analysis for SSVEP paradigm"""
    def __init__(self, freqs, win_len, s_rate, n_harmonics=1):
        """
        Args:
            freqs (list): List of target frequencies
            win_len (float): Window length
            s_rate (int): Sampling rate of EEG signal
            n_harmonics (int): Number of harmonics to be considered
        """
        self.freqs = freqs
        self.win_len = win_len
        self.s_rate = s_rate
        self.n_harmonics = n_harmonics
        self.train_data = self._init_train_data()
        self.cca = CCA(n_components=1)

    def _init_train_data(self):
        t_vec = np.linspace(0, self.win_len, int(self.s_rate * self.win_len))
        targets = {}
        for freq in self.freqs:
            sig_sin, sig_cos = [], []
            for harmonics in range(self.n_harmonics):
                sig_sin.append(np.sin(2 * np.pi * harmonics * freq * t_vec))
                sig_cos.append(np.cos(2 * np.pi * harmonics * freq * t_vec))
            targets[freq] = np.array(sig_sin + sig_cos).T
        return targets

    def apply_cca(self, eeg):
        """Apply CCA analysis to EEG data and return scores for each target frequency

        Args:
            eeg (np.array): EEG array [n_samples, n_chan]

        Returns:
            list of scores for target frequencies
        """
        scores = []
        for key in self.train_data:
            sig_c, t_c = self.cca.fit_transform(eeg, self.train_data[key])
            scores.append(np.corrcoef(sig_c.T, t_c.T)[0, 1])
        return scores