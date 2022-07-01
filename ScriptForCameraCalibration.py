from __future__ import print_function
from CalibrationPattern import ChessBoard
from Camera import DummyDevice
import cv2

device = DummyDevice.DummyDevice()

print(device)
frequencyOfPatternFound = 1


while(True):
    colorFrame = device.getColorFrame()
    checkerBoard = ChessBoard.ChessBoard(RGB=colorFrame)
    checkerBoard.show()
    checkerBoard.showGray()
    patternFound = checkerBoard.calculateObjectnImagePointsnDisplay(drawCorners = True)
    if patternFound:
        checkerBoard.save()
        frequencyOfPatternFound = frequencyOfPatternFound + 1

        if frequencyOfPatternFound > 5:
            break

print(device.calibrate(checkerBoard.getObjectPoints(), checkerBoard.getImagePoints(), checkerBoard.getGrayScaleShape()))
