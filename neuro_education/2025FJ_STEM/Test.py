import mne
import pandas as pd


def import_eeg_raw_unicorn(path):
    # Define the channel names (EEG channels only)
    ch_names = ['Fz', 'C3', 'Cz', 'C4', 'P2', 'PO7', 'Oz', 'PO8']
    counter = 'Time'
    all_ch_names = ch_names + [counter]

    sfreq = 250  # Unicorn default sampling rate

    # Load the CSV
    eeg_pandas = pd.read_csv(path)

    # Select the first 8 columns (EEG) + and the last one (time)
    eeg_pandas = eeg_pandas.iloc[:, list(range(8)) + [-1]]

    #Transpose and fill with NaNs
    eeg_pandas = eeg_pandas.fillna(0).transpose()

    # Create MNE Info with EEG and aux channel types
    ch_types = ['eeg'] * len(ch_names) + ['misc']  # 'Time' as misc
    eeg_info = mne.create_info(all_ch_names, sfreq, ch_types=ch_types, verbose=None)

    # Create Raw object
    eeg_raw = mne.io.RawArray(eeg_pandas.values, eeg_info)

    # Apply standard 10-20 montage
    montage_1020 = mne.channels.make_standard_montage("standard_1020", head_size='auto')
    eeg_raw.set_montage(montage_1020, match_case=False)

    return eeg_raw
raw = import_eeg_raw_unicorn('/Users/monicamayorga/Downloads/eeg.csv')