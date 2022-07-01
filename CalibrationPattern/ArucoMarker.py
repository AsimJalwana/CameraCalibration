import itertools

import cv2 as openCV
import numpy as np
from cv2 import aruco

from CalibrationPattern import AbstractCalibrationPattern


class ArucoMarker(AbstractCalibrationPattern.AbstractCalibrationPattern):
    __criteria = (openCV.TERM_CRITERIA_EPS + openCV.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    __MARKER_LENGTH = 79 # in millimeters

    def __init__(self, **kwargs):
        super(ArucoMarker, self).__init__(**kwargs)
        super(ArucoMarker, self).setGrayFileNamePrefix("ArucoImageGray")
        super(ArucoMarker, self).setRGBFileNamePrefix("ArucoImageRGB")
        self.__parameters = aruco.DetectorParameters_create()
        self.__aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_1000)

    def findPoseOfPattern(self, cameraParams):
        cornersFound = False
        self.__corners, ids, rejectedImgPoints = aruco.detectMarkers(self.changeToGray(), self.__aruco_dict, parameters=self.__parameters)
        K = cameraParams.getIntrinsicMatrix()
        distortion = cameraParams.getDistortion()
        rvec = []
        tvec = []
        if ids != None:  # if aruco marker detected
            rvec, tvec, _objectPoints = aruco.estimatePoseSingleMarkers(self.__corners, self.__MARKER_LENGTH, K, distortion)  # For a single marker
            imgWithAruco = aruco.drawDetectedMarkers(self._SHAPE_OF_GRAYSCALE, self.__corners, ids, (0, 255, 0))
            imgWithAruco = aruco.drawAxis(imgWithAruco, K, distortion, rvec, tvec, 100)  # axis length 100 can be changed according to your requirement
            openCV.imshow("Aruco", imgWithAruco)

        rvec = np.transpose(list(itertools.chain(*rvec)))
        tvec = np.transpose(list(itertools.chain(*tvec)))
        return rvec, tvec

    def calculateObjectnImagePointsnDisplay(self, drawCorners = True, aggregateToList = True):
        print("Its in development phase, Please wait for next code update.")