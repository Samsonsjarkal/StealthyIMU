# StealthyIMU: Stealing Permission-protected Private Information From Smartphone Voice Assistant Using Zero-Permission Sensors, NDSS 2023

[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Samsonsjarkal/StealthyIMU/blob/master/LICENSE) 
[![](https://img.shields.io/github/stars/Samsonsjarkal/StealthyIMU.svg)](https://github.com/Samsonsjarkal/StealthyIMU/stargazers)
[![](https://img.shields.io/github/forks/Samsonsjarkal/StealthyIMU.svg)](https://github.com/Samsonsjarkal/StealthyIMU/network) 

StealthyIMU is a privacy threat that uses motion sensors to steal permission-protected private information from the Voice User Interfaces (VUIs) on smartphone. StealthyIMU can steal private information from 23 types of frequently-used voice commands to acquire contacts, search history, calendar, home address, and even GPS trace with high accuracy. Please refer to [our StealthyIMU paper](https://github.com/Samsonsjarkal/KeSun/blob/master/files/ndss23_StealthyIMU.pdf) in NDSS 2023 for more details. 

In this repo, we release our collected VUI response dataset, which contains the ground truth permission-protected private entities, audio recording, and corresponding accelerometer and gyroscope signals for each VUI response. Besides, we open-source the basic Spoken Language Model (SLU) DNN model that steals the permission-protected private entities from the motion sensor signals on smartphone.

![stealthyimu](https://github.com/Samsonsjarkal/KeSun/blob/master/img/stealthyimu.jpg)

## Dataset Preparation
Our open-sourced dataset contains 7 types of VUI responses as shown in the following table.

| Type          | Example VUI Response | Privacy | # |
| ------------- | ---------------------|---------|---|
| Weather        | Time in **San Diego** California is 10:33 P.M.| Location | 12527 |
| Sun set&rise   | In **New York City** today the sun will set at 4:42 P.M. | Location | 1493 |
| AirCheck       | According to the air quality near the center of **Phoenix** <br />is good with and index ranging from 27 to 41. | Location | 843 |
| Clock          | Time in **Tusla** Oklahoma United States is **12:31 A.M. on Tuesday**. | Location, Time | 1593 |
| Reminder       | **Order Groceries**. When do you want to be reminded? | Todo | 2950 |
| Reminder       | All right. I will remind you on **Monday at 7 P.M.** | Time | 2081 |
| Stock          | **Apple** closed down 1.5% at $153.34. | Search History | 1318 |
| Navigation <br />(San Diego) | Use the left two lanes to **turn left** onto **Convoy Street** | GPS trace | 5096 |
| Navigation <br />(New York)  | In a quarter mile **turn left** onto **Hancock Place** | GPS trace | 2794 |


For each VUI response, we provide the following information:
- Metadata: ground truth of permission-protected private entities, transcription of audio recording 
- Motion Sensor Signals (MSS): 6 DoF accelerometer (.acc) and gyroscope (.gyro) signals 
- Audio Recordings: the audio (.wav) recorded by microphone on an Macbook Pro laptop
- Transcription File: the transcription file (.txt) of audio recordings via Amazon Transcribe or Google Speech-to-text
- The MSS signals after normalization (.accnpy, .gyronpy)
- The GPS trace/ location for the navigation command (.gps)

The dataset can be downloaded from the [Google Drive](https://drive.google.com/file/d/18wBg8mehJZ0gLW6O8T7fkq53J-8EQLdJ/view?usp=sharing).


## Prerequisites and Training

Our implentation is based on the [SpeechBrain](https://github.com/speechbrain/speechbrain)
Once you have created your Python environment (Python 3.7+), you can install the SpeechBrain via pip.

```pip install speechbrain```

Then make sure that you can access SpeechBrain with:

```import speechbrain as sb```

We provide [a pretrained baseline Spoken Language Understanding (SLU) model and results](https://drive.google.com/file/d/19b3LzaoLIGkdDrxYYxV9NhARg_Bw_z4b/view?usp=sharing). 

You can also train a baseline Spoken Language Understanding (SLU) model for StealthyIMU with:

```python train.py hparams/baseline.yaml```

Note that
- You may need to change the "data_folder" in ["hparams/baseline.yaml"](https://github.com/Samsonsjarkal/StealthyIMU/blob/main/hparams/open_source.yaml) to your download folder. If you want to modify more parameters in the model, please refer to ["hparams/baseline.yaml"](https://github.com/Samsonsjarkal/StealthyIMU/blob/main/hparams/open_source.yaml).

- The pretrained tokenizer is provided in the file folder ["pretrain"](https://github.com/Samsonsjarkal/StealthyIMU/blob/main/pretrain). If you want to train a tokenizer by your self, please refer to [SpeechBrain SLURP](https://github.com/speechbrain/speechbrain/tree/develop/recipes/SLURP). 



## Evaluation Tool and Baseline Results

Once you train and test the model. You will receive a testing result ["wer_test_real.txt"](https://github.com/Samsonsjarkal/StealthyIMU/blob/main/results/BPE51_all_opensource/1235/wer_test_real.txt).

You can evaluate StealthyIMU via our evaluation tool with

```python eval/eval.py ./results/BPE51_all_opensource/1235/wer_test_real.txt```

Here is an example results of our baseline model. You can improve this baseline results by designing a better SLU model or balance different types of VUI response data in the training dataset as discussed in [our StealthyIMU paper](https://github.com/Samsonsjarkal/KeSun/blob/master/files/ndss23_StealthyIMU.pdf).

| Type          | TER | SER | SEER |
| ------------- | --- | --- | ---- |
| Weather        | 0.0% | 2.5%  | 1.2% | 
| Sun set&rise   | 0.0% | 12.0% | 6.0% |
| AirCheck       | 0.0% | 7.8%  | 3.9% |
| Clock          | 0.0% | 1.8%  | 0.9% |
| Reminder (Todo)| 0.0% | 18.8% | 9.4% |
| Reminder (Time)| 0.0% | 29.7% | 14.9% |
| Stock          | 0.0% | 31.3% | 15.7% |
| Navigation     | 0.0% | 38.6% | 15.9% |
| Overall        | 0.0% | 16.5% | 8.5% |

## Citing StealthyIMU 
Ke Sun, Chunyu Xia, Songlin Xu, Xinyu Zhang. StealthyIMU: Extracting Permission-protected Private Information from Smartphone Voice Assistant using Zero-Permission Sensors. In Proceedings of NDSS, 2023

```bibtex
@inproceedings{sun2023stealthyimu,
  title={{StealthyIMU}: Extracting Permission-protected Private Information from Smartphone Voice Assistant using Zero-Permission Sensors,
  author={Sun, Ke and Xia, Chunyu and Xu, Songlin and Zhang, Xinyu},
  year={2023},
  booktitle={NDSS},
}
```
