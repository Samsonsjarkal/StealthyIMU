import os
import jsonlines
from speechbrain.dataio.dataio import read_audio, merge_csvs
from speechbrain.utils.data_utils import download_file
import shutil
import csv
from sklearn.model_selection import train_test_split
import numpy as np
import random

try:
    import pandas as pd
except ImportError:
    err_msg = (
        "The optional dependency pandas must be installed to run this recipe.\n"
    )
    err_msg += "Install using `pip install pandas`.\n"
    raise ImportError(err_msg)


def prepare_StealthyIMU(
    data_folder, file_name, save_folder, slu_type, train_splits, skip_prep=False, seed=1234
):
    """
    This function prepares the StealthyIMU dataset.

    data_folder : path to StealthyIMU dataset. Currently only two folders: \Mocklocation_clean, \Reminder_S2T_All_Reuid
    save_folder: path where to save the csv manifest files.
    slu_type : one of the following:

      "direct":{input=audio, output=semantics}
      "multistage":{input=audio, output=semantics} (using ASR transcripts in the middle)
      "decoupled":{input=transcript, output=semantics} (using ground-truth transcripts)

    split the dataset to train (8), valid (1), test (1)
    """
    if skip_prep:
        return

    filename = os.path.join(data_folder, file_name)
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_reader = list(csv_reader)

    random.seed(seed)
    values = np.linspace(0, len(csv_reader) -1 , len(csv_reader), dtype=int)
    random.shuffle(values)
    training_dataset, testing_dataset = train_test_split(values, train_size= int(len(csv_reader) * 0.8), test_size=len(csv_reader) - int(len(csv_reader) * 0.8))
    validing_dataset = testing_dataset[0:int(len(testing_dataset)/2)]
    testing_dataset = testing_dataset[int(len(testing_dataset)/2):]
    
    splits = [
        "train",
        "test",
        "valid"
    ]

    for split in splits:
        new_filename = (
            os.path.join(save_folder, split) + "-type=%s.csv" % slu_type
        )
        if os.path.exists(new_filename):
            continue
        print("Preparing %s..." % new_filename)

        if (split == "train"):
            list_now = training_dataset
            print(len(list_now))
        elif (split == "test"):
            list_now = testing_dataset
        elif (split == "valid"):
            list_now = validing_dataset

        IDs = []
        duration = []
        wav = []
        semantics = []
        transcript = []

        for data_id in list_now:
            data_sample = csv_reader[data_id]
            IDs.append(data_sample[0])
            duration.append(data_sample[1])
            wav.append(data_sample[2])
            semantics.append(data_sample[3])
            transcript.append(data_sample[4][:-1])
        
        df = pd.DataFrame(
                {
                    "ID": IDs,
                    "duration": duration,
                    "wav": wav,
                    "semantics": semantics,
                    "transcript": transcript,
                }
            )
        df.to_csv(new_filename, index=False)

