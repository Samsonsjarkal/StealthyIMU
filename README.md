# StealthyIMU: Stealing Permission-protected Private Information From Smartphone Voice Assistant Using Zero-Permission Sensors, NDSS 2023

StealthyIMU is a privacy threat that uses motion sensors to steal permission-protected private information from the Voice User Interfaces (VUIs) on smartphone. StealthyIMU can steal private information from 23 types of frequently-used voice commands to acquire contacts, search history, calendar, home address, and even GPS trace with high accuracy. Please refer to our [StealthyIMU](https://github.com/Samsonsjarkal/KeSun/blob/master/files/ndss23_StealthyIMU.pdf) paper in NDSS 2023 for more details. 

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
| Stock          | | Search History | 1318 |
| Navigation <br />(San Diego) | Use the left two lanes to **turn left** onto **Convoy Street** | GPS trace | 5096 |
| Navigation <br />(New York)  | In a quarter mile **turn left** onto **Hancock Place** | GPS trace | 2794 |


For each VUI response, we provide the following information:
- Metadata: ground truth of permission-protected private entities, transcription of audio recording 
- Motion Sensor Signals (MSS): 6 DoF accelerometer (.acc) and gyroscope (.gyro) signals 
- Audio Recordings: the audio (.wav) recorded by microphone on an Macbook Pro laptop
- Transcription File: the transcription file (.txt) of audio recordings via Amazon Transcribe or Google Speech-to-text
- The MSS signals after normalization (.accnpy, .gyronpy)
- The GPS trace/ location for the navigation command (.gps)

The dataset can be downloaded from the [Google Drive]().


## Dataset Preparation

## Evaluation Tool
## Baseline models and results

## Reference 
Ke Sun, Chunyu Xia, Songlin Xu, Xinyu Zhang. StealthyIMU: Extracting Permission-protected Private Information from Smartphone Voice Assistant using Zero-Permission Sensors. In Proceedings of NDSS, 2023
