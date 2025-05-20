import mne
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mne_bids import write_raw_bids, BIDSPath


class eeg:
    def __init__(self, path):
        self.path = path

    def import_eeg_raw_unicorn(self):
        # Define the channel names (EEG channels only)
        ch_names = ['Fz', 'C3', 'Cz', 'C4', 'P2', 'PO7', 'Oz', 'PO8']
        counter = 'Time'
        all_ch_names = ch_names + [counter]

        sfreq = 250  # Unicorn default sampling rate

        # Load the CSV
        eeg_pandas = pd.read_csv(self.path)

        # Select the first 8 columns (EEG) + and the last one (time)
        eeg_pandas = eeg_pandas.iloc[sfreq*3:, list(range(8)) + [-1]].reset_index(drop=True) #remove first 3 seconds of every record

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

        print(print(eeg_pandas.info()))

        self.eeg_raw = eeg_raw
        self.current_eeg = eeg_raw
    
    def filter(self,type, eeg_object):
        if type == 'notch':
            self.apply_notch_filter(eeg_object, freqs=[60], notch_width=2.0)
        elif type == 'highpass':
            self.hpf_function(eeg_object)
        else:
            print("ERROR - fitler type not recognized")
    
    def hpf_function(self, eeg_object):
        self.current_eeg = eeg_object.copy()
        self.current_eeg.filter(
            l_freq=1,
            h_freq=None,
            fir_window='hamming',
            fir_design='firwin',
            phase='zero-double',  # Ensures 50% overlap (zero-phase with 2x filtering)
            filter_length=830 ,    # FIR filter order + 1 (length = order + 1)
            verbose=False
        )

    def apply_notch_filter(self, eeg_object,  freqs=[60], notch_width=2.0):
        self.current_eeg = eeg_object.copy()
        self.current_eeg.notch_filter(
            freqs=freqs,
            notch_widths=notch_width,
            method='fir',
            fir_design='firwin',
            phase='zero-double',  # 50% overlap = zero-phase filtering applied twice
            fir_window='hamming',
            verbose=False
        )
    
    def export_to_bids(self, bids_root, subject_id='01', session='01', task='rest', run='01'):
        bids_path = BIDSPath(
            root=bids_root,
            subject=subject_id,
            session=session,
            task=task,
            run=run,
            datatype='eeg'
        )

        write_raw_bids(
            raw=self.eeg_raw,
            allow_preload=True,
            bids_path=bids_path,
            overwrite=True,
            format='BrainVision'  # recommended format for EEG
        )

        print(f"BIDS export complete at: {bids_path.fpath.parent}")

if __name__ == "__main__":
    dirs = ("1XL74fi7YxV5-U0nXM1CqQU5051UR3I3m","STEM")