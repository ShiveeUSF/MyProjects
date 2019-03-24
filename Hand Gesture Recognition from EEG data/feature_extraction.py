#Importing packages
import numpy as np
import pandas as pd

from mne.io import RawArray
from mne.channels import read_montage
from mne.epochs import concatenate_epochs
from mne import create_info, find_events, Epochs, concatenate_raws, pick_types, EpochsArray, EvokedArray
from mne.decoding import CSP

from scipy.signal import butter, lfilter, convolve, boxcar
from joblib import Parallel, delayed
from glob import glob

import warnings

warnings.filterwarnings('ignore')


def creat_mne_raw_object(fname, read_events=True):
    """
    Creates a mne raw instance from csv file
    Arguments
    fname:  file path
    read_events: boolean indicating whether we want to read events file
    """

    data = pd.read_csv(fname)
    # get chanel names
    ch_names = list(data.columns[1:])
    # read EEG standard montage from mne
    montage = read_montage('standard_1005', ch_names)
    ch_type = ['eeg'] * len(ch_names)
    data = 1e-6 * np.array(data[ch_names]).T
    if read_events:
        ev_fname = fname.replace('_data', '_events')
        events = pd.read_csv(ev_fname)
        events_names = events.columns[1:] #ignore id column
        events_data = np.array(events[events_names]).T
        # define channel type, the first is EEG, the last 6 are stimulations
        ch_type.extend(['stim'] * 6)
        ch_names.extend(events_names)
        # concatenate event file and data
        data = np.concatenate((data, events_data))

    # create and populate MNE info structure
    info = create_info(ch_names, sfreq=500.0, ch_types=ch_type, montage=montage)
    info['filename'] = fname
    # create raw object
    raw = RawArray(data, info, verbose=False)
    return raw

# Declaring and initializing variables
subjects = range(1, 13)
ids_tot = []
pred_tot = []
# designing butterworth bandpass filters
freqs = [7, 30]
nr_lowpass = 5
b, a = butter(5, np.array(freqs) / 250.0, btype='bandpass')
b_low, a_low = butter(5, (0.2) / 250.0, btype='lowpass')
b_low1, a_low1 = butter(5, (0.4) / 250.0, btype='lowpass')
b_low2, a_low2 = butter(5, (0.6) / 250.0, btype='lowpass')
b_low3, a_low3 = butter(5, 1 / 250.0, btype='lowpass')

# CSP parameters
# Number of spatial filter to use
nfilters = 4
# convolution window for smoothing features
nwin = 250
# training subsample
subsample = 10
cols = ['HandStart', 'FirstDigitTouch', 'BothStartLoadPh', 'LiftOff', 'Replace', 'BothReleased'] #hand gestures

# Extracting features for each subject for each event
for subject in subjects:
    epochs_tot = []
    y = []
    ################ Read data #####################################

    fnames = glob('subj%d_series*_data.csv' % (subject)) #read all files for that subject
    # concatenate into one object per subject
    raw = concatenate_raws([creat_mne_raw_object(fname) for fname in fnames])
    # pick eeg signal
    picks_data = pick_types(raw.info, eeg=True)
    # Filter data for alpha frequency and beta band
    # MNE implement a zero phase filtering not compatible with the rule of future data.
    # Hence we use left filter compatible with this constraint.
    # The function parallelized for speeding up the script

    low_feat = np.zeros(np.shape(raw._data))
    low_feat1 = np.zeros(np.shape(raw._data))
    low_feat2 = np.zeros(np.shape(raw._data))
    low_feat3 = np.zeros(np.shape(raw._data))
    low_feat[picks_data] = np.array(Parallel(n_jobs=-1)(delayed(lfilter)(b_low, a_low, raw._data[i])
                                                        for i in picks_data))
    low_feat1[picks_data] = np.array(Parallel(n_jobs=-1)(delayed(lfilter)(b_low1, a_low1, raw._data[i])
                                                         for i in picks_data))
    low_feat2[picks_data] = np.array(Parallel(n_jobs=-1)(delayed(lfilter)(b_low2, a_low2, raw._data[i])
                                                         for i in picks_data))
    low_feat3[picks_data] = np.array(Parallel(n_jobs=-1)(delayed(lfilter)(b_low3, a_low3, raw._data[i])
                                                         for i in picks_data))
    raw._data[picks_data] = np.array(Parallel(n_jobs=-1)(delayed(lfilter)(b, a, raw._data[i])
                                                         for i in picks_data))

    ################ CSP Filters training #####################################

    # getting epochs for Replace event
    events_1 = find_events(raw, stim_channel='Replace', verbose=False)
    epochs_1 = Epochs(raw, events_1, {'Replace': 1}, -0.2, 0.8, proj=False,
                      picks=picks_data, baseline=None, preload=True, verbose=False)

    epochs_tot.append(epochs_1)
    y.extend([1] * len(epochs_1))

    # getting epochs for Handstart event
    events_2 = find_events(raw, stim_channel='HandStart', verbose=False)
    epochs_2 = Epochs(raw, events_2, {'HandStart': 1}, -0.2, 0.8, proj=False,
                      picks=picks_data, baseline=None, preload=True, verbose=False)

    epochs_tot.append(epochs_2)
    y.extend([2] * len(epochs_2))

    # getting epochs for FirstDigitTouch event
    events_3 = find_events(raw, stim_channel='FirstDigitTouch', verbose=False)
    epochs_3 = Epochs(raw, events_3, {'FirstDigitTouch': 1}, -0.2, 0.8, proj=False,
                      picks=picks_data, baseline=None, preload=True, verbose=False)

    epochs_tot.append(epochs_3)
    y.extend([3] * len(epochs_3))

    # BothStartLoadPhase
    events_4 = find_events(raw, stim_channel='BothStartLoadPh', verbose=False)
    epochs_4 = Epochs(raw, events_4, {'BothStartLoadPh': 1}, -0.2, 0.8, proj=False,
                      picks=picks_data, baseline=None, preload=True, verbose=False)

    epochs_tot.append(epochs_4)
    y.extend([4] * len(epochs_4))

    # LiftOff
    events_5 = find_events(raw, stim_channel='LiftOff', verbose=False)
    epochs_5 = Epochs(raw, events_5, {'LiftOff': 1}, -0.2, 0.8, proj=False,
                      picks=picks_data, baseline=None, preload=True, verbose=False)

    epochs_tot.append(epochs_5)
    y.extend([5] * len(epochs_5))

    # BothReleased
    events_6 = find_events(raw, stim_channel='BothReleased', verbose=False)
    epochs_6 = Epochs(raw, events_6, {'BothReleased': 1}, -0.2, 0.8, proj=False,
                      picks=picks_data, baseline=None, preload=True, verbose=False)

    epochs_tot.append(epochs_6)
    y.extend([6] * len(epochs_6))

    # Concatenate all epochs
    epochs = concatenate_epochs(epochs_tot)

    # get training features and labels
    X = epochs.get_data()
    y = np.array(y)

    # train CSP
    csp = CSP(n_components=nfilters, reg='ledoit_wolf')
    csp.fit(X, y)

    ################ Create Training Features #################################
    # apply csp filters and rectify signal
    feat = np.dot(csp.filters_[0:nfilters], raw._data[picks_data]) ** 2
    feat1 = np.dot(csp.filters_[0:nfilters], low_feat[picks_data]) ** 2
    feat2 = np.dot(csp.filters_[0:nfilters], low_feat1[picks_data]) ** 2
    feat3 = np.dot(csp.filters_[0:nfilters], low_feat2[picks_data]) ** 2
    feat4 = np.dot(csp.filters_[0:nfilters], low_feat3[picks_data]) ** 2

    # smoothing by convolution with a rectangle window
    feattr = np.concatenate((feat, feat1, feat2, feat3, feat4), axis=0)

    labels = raw._data[32:]
    features_labels = np.concatenate((labels, feattr), axis=0).T

    # Write features and labels to a csv file
    submission = pd.DataFrame(features_labels)
    submission.to_csv('subj%d_series_data.csv' % (subject),
                      index_label='id', float_format='%.5f')

