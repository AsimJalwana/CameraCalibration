from __future__ import print_function
import abc
import cv2 as openCV
from Utilities import Utilities
import os
import numpy as np

class AbstractCalibrationPattern(object):
    __metaclass__ = abc.ABCMeta
    __IMAGES_STORE_PATH = ".\\CapturedImages"
    __imagePostFix = 1
    _SHAPE_OF_GRAYSCALE = None
    _ListOfDetectedObjectPoints = []
    _ListOfDetectedImagePoints = []

    def __init__(self,**kwargs):
        self._fileName = kwargs.get('fileName')
        self._image = kwargs.get('RGB')
        self._gray = None
        self._corners = None
        self._rgbfileNamePrefix = "ImageRGB"
        self._grayfileNamePrefix = "ImageGray"
        return

    def setRGBFileNamePrefix(self, prefix):
        self._rgbfileNamePrefix = prefix

    def setGrayFileNamePrefix(self, prefix):
        self._grayfileNamePrefix = prefix

    def toString(self):
        return self._fileName

    def read(self):
        if self._fileName is not None:
            self._image = openCV.imread(self._fileName)

    def show(self):
        if self._image is None:
            self.read()

        Utilities.Utils.imshow(self._image, waitKey=1000)

    def changeToGray(self):
        if self._gray is not None:
            return self._gray

        if self._image is None:
            self.read()

        self._gray = openCV.cvtColor(self._image, openCV.COLOR_BGR2GRAY)
        AbstractCalibrationPattern._SHAPE_OF_GRAYSCALE = self._gray.shape

    def showGray(self):
        if self._gray is None:
            self.changeToGray()

        Utilities.Utils.imshow(self._image, waitKey=1000)

    def saveGray(self):
        if self._gray is None:
            self.changeToGray()

        fileName = self._fileName

        if fileName is None:
            fileName = self._grayfileNamePrefix

        fileName = fileName + str(AbstractCalibrationPattern.__imagePostFix) + ".jpg"
        AbstractCalibrationPattern.__imagePostFix = AbstractCalibrationPattern.__imagePostFix + 1
        openCV.imwrite(os.path.join(self.__IMAGES_STORE_PATH, fileName), self._image)

    def save(self):
        fileName = self._fileName
        if fileName is None:
            fileName = self._rgbfileNamePrefix
        fileName = fileName + str(AbstractCalibrationPattern.__imagePostFix) + ".jpg"
        AbstractCalibrationPattern.__imagePostFix = AbstractCalibrationPattern.__imagePostFix + 1
        openCV.imwrite(os.path.join(self.__IMAGES_STORE_PATH, fileName), self._image)

    @abc.abstractmethod
    def findPoseOfPattern(self, cameraParams):
        """
            Find the pose and return the rotation and translation vectors
        """

    def rotationVector2Matrix(self, rvec):
        rotation_matrix = np.zeros(shape=(3, 3))
        rotation_matrix, _ = openCV.Rodrigues(rvec, rotation_matrix)
        return rotation_matrix

    @abc.abstractmethod
    def calculateObjectnImagePointsnDisplay(self, drawCorners = True, aggregateToList = True):
        """
            Find the corresponding World Coordinates and corresponding pixels
        """