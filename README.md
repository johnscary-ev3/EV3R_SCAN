# EV3R_SCAN
EV3RSTORM program with just object detection and scanning motor heads using threads
Sensor ports are listed in main.py and head motors use Ports A and D.
Motors need a hard stop between 50 and 90 degrees from the front direction.
Stop direction can be on either side and is configured in the main.py file.
Also the degrees offset from front direction is configured in main.py file.
Motors will go to the stop and then reposition using the offset.
Then they will re-zero and all moves after will be relative to that new zero point.
After scanning starts, objects <300cm will trigger a detected Yellow light and an audio detected message.
Program can be stopped using Beacon button on IR remote. Any channel.
