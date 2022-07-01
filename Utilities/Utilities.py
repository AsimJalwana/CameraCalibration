import cv2 as openCV
import numpy as np
import os
import time
import datetime

class Utils:
    __randomCounter = 1;

    @classmethod
    def imshow(cls, image, name = "Image" + str(__randomCounter), waitKey=0):
        openCV.namedWindow(name, openCV.WND_PROP_FULLSCREEN)
        openCV.setWindowProperty(name, openCV.WND_PROP_FULLSCREEN, openCV.WINDOW_FULLSCREEN)
        openCV.imshow(name, image)
        openCV.waitKey(waitKey)
        openCV.destroyAllWindows()

    @classmethod
    def getTimestampAsString(cls):
        return datetime.datetime.now().strftime("%d-%m-%Y--%H%M%S")
    