import numpy as np
import cv2
import glob
import os
from CalibrationPattern import ChessBoard
from Camera import Device


class DummyDevice(Device.Device):
    __COLOR_IMAGES_STORE_PATH = None
    __path = None
    __path = None
    __images = None
    __index = None

    def __init__(self):
        self.__COLOR_IMAGES_STORE_PATH = ".\CapturedImages"
        self.__path = self.__COLOR_IMAGES_STORE_PATH
        self.__path = os.path.join(self.__path, "*.jpg")
        self.__images = glob.glob(self.__path)
        self.__index = 0

    def getColorFrame(self):
        if self.__index >= len(self.__images):
            return None

        fileName = self.__images[self.__index]
        self.__index = self.__index + 1
        print("FileName is :: ", fileName)
        rgbImage = cv2.imread(fileName)
        return rgbImage
