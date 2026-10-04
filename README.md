# Detection of state of a machine using opencv-python
This project detects when a machine (in this case a fan) is RUNNING or STOPPED.
# Requirements:
- Python
- OpenCV
- Numpy
# What it does:
- From the video, it figures out the ROI from video properties
- It detects motion in the video
- It then states when the machine (fan) is stopped or running
- Accurate
# How it works:
A video of a fan is uploaded onto OpenCV
The region around the fan blades is noted as ROI
Pixel changes caused due to consecutive frame changes are noted down
A motion threshold determines whether the fan is moving or not
# Results
The system is classified into "RUNNING" or "STOPPED"

## Future Improvements:
- Machine Learning based detection