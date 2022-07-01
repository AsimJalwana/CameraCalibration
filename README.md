# Camera Calibration

## Getting Started
This is a PyCharm project that does the following tasks
*   Calibration of any RGB camera. 

Many different patterns are used for calibration. The most commonly used patterns include checkerboard and the circle pattern. This software has the support for the Checkerboard/Chessboard. 

### Prerequisites
* Windows 10
* Python 3.8 
* opencv 4.5.5
* numpy 1.22.3 
* scipy 1.8.0

### How to Run this Software?
First we need a calibration pattern. One can download it from https://markhedleyjones.com/projects/calibration-checkerboard-collection and print it out. Please note 
that one needs to paste the pattern on a card board or any flat surface to keep it flat. The code assumes that. 

Take many photographs of the Calibration patern from the camera and place it in folder 'CapturedImages'. Once done, kindly check
```CameraCalibration\ChessBoard.py``` and set the ```___BLOCK_SIZE_MM``` on Line 10. This variable accepts the size of pattern block in millimetres.

That is all the setting! 

The code can be run as 
```python
python ScriptForCameraCalibration.py
```
It will print out the calibration matrices as well as save it in folder ```savedCameraCalibration```


More details are shared on the Wiki page. Please refer to it.

