import pickle
from Utilities import Utilities
import os
import numpy as np
import scipy
from scipy import io
from CalibrationPattern import ChessBoard


class CameraParams:
    __SAVE_DIRECTORY = ".//SavedCameraParameters"

    def __init__(self):
        self.__intrinsicMatrix = []
        self.__distortion = []
        self.__rotation = []
        self.__translation = []
        self.__reProjectionError = None
        self.__resolution = None

    def toDict(self, rotationVector=None, translationVector=None, dict=None, ):
        if dict is None:
            dict = {}
            dict["IntrinicMatrix"] = np.transpose(self.__intrinsicMatrix)
            dict["RadialDistortion"] = [self.__distortion[0][0], self.__distortion[0][1], self.__distortion[0][4]]
            dict["TangentialDistortion"] = [self.__distortion[0][2], self.__distortion[0][3]]
            dict["ImageSize"] = self.__resolution
            dict["WorldPoints"] = ChessBoard.ChessBoard.getObjectPointsGrid()[:, 0:2]

        if rotationVector is not None:
            if dict.get("RotationVectors") is None:
                dict["RotationVectors"] = np.transpose(rotationVector)
            else:
                dict["RotationVectors"] = np.append(dict["RotationVectors"], np.transpose(rotationVector), axis=0)

        if translationVector is not None:
            if dict.get("TranslationVectors") is None:
                dict["TranslationVectors"] = np.transpose(translationVector)
            else:
                dict["TranslationVectors"] = np.append(dict["TranslationVectors"], np.transpose(translationVector),axis=0)

        return dict

    def getResolution(self):
        return self.__resolution

    def setResolution(self, resolution):
        self.__resolution = np.array(resolution, dtype='float32')

    def getReProjectionError(self):
        return self.__reProjectionError

    def setReProjectionError(self, error):
        self.__reProjectionError = error

    def getIntrinsicMatrix(self):
        return self.__intrinsicMatrix

    def getDistortion(self):
        return self.__distortion

    def getRotation(self):
        return self.__rotation

    def getTranslation(self):
        return self.__translation

    def setIntrinsicMatrix(self, intrinsicMatrix):
        self.__intrinsicMatrix = np.array(intrinsicMatrix, 'float32')

    def setDistortion(self, distortion):
        self.__distortion = np.array(distortion, 'float32')

    def setRotation(self, rotation):
        self.__rotation = np.array(rotation, 'float32')

    def setTranslation(self, translation):
        self.__translation = np.array(translation, 'float32')

    def display(self):
        print("Reprojection Error is :: ", self.__reProjectionError)
        print("IntrinsicMatrix is :: ", self.__intrinsicMatrix)
        print("Distortion is :: ", self.__distortion)
        print("Rotation is :: ", self.__rotation)
        print("Translation is :: ", self.__translation)

    def save(self):
        fileName = "CameraParams_" + Utilities.Utils.getTimestampAsString() + '.pkl'

        if not os.path.exists(self.__SAVE_DIRECTORY):
            os.makedirs(self.__SAVE_DIRECTORY)

        with open(os.path.join(self.__SAVE_DIRECTORY, fileName), 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
        pass

    @classmethod
    def loadCameraParameters(cls, fileName):
        params = None
        with open(os.path.join(cls.__SAVE_DIRECTORY, fileName), 'rb') as input:
            params = pickle.load(input)
        return params
