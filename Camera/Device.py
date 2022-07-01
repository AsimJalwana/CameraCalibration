from __future__ import print_function
import abc
import cv2 as openCV
from Camera import CameraParams

class Device(object):
    __metaclass__ = abc.ABCMeta
    __parameters = CameraParams.CameraParams()

    def __init__(self):
        return

    @abc.abstractmethod
    def getColorFrame(self):
        """
            Grab the color (RGB) frame from the device for returning it.
            :return: color frame
        """

    @classmethod
    def calibrate(cls, objectPoints, imagePoints, imageShape):
        """
            :param objectPoints: The object Points in 3D coordinate System
            :param imagePoints: The pixel Position of the Object Points.
            :param imageShape: Rows by columns in the Image
            :return: it saves the parameters in the Class variable __parameters
        """
        ret, mtx, dist, rvecs, tvecs =  openCV.calibrateCamera(objectPoints, imagePoints, imageShape[::-1], None, None)

        print("ret" , ret)
        print("mtx ", mtx)
        print("rvecs ", rvecs)
        print("tvecs ", tvecs)

        cls.__parameters.setReProjectionError(ret)
        cls.__parameters.setIntrinsicMatrix(mtx)
        cls.__parameters.setDistortion(dist)
        cls.__parameters.setRotation(rvecs)
        cls.__parameters.setTranslation(tvecs)
        cls.__parameters.setResolution(imageShape)
        cls.__parameters.display()
        cls.__parameters.save()


    @classmethod
    def findOptimalMatrixAfterCalibration(cls, intrinsicMatrix, distortion, imageShape):
        print(openCV.getOptimalNewCameraMatrix(intrinsicMatrix, distortion, imageShape, 1, imageShape))

    @classmethod
    def getDeviceParameters(cls):
        return cls.__parameters