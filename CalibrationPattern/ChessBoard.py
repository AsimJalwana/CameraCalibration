import cv2 as openCV
import numpy as np
from Utilities import Utilities
from CalibrationPattern import AbstractCalibrationPattern

class ChessBoard(AbstractCalibrationPattern.AbstractCalibrationPattern):
    __rows = 7
    __cols = 9
    __criteria = (openCV.TERM_CRITERIA_EPS + openCV.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    __BLOCK_SIZE_MM = 22 # in millimeters
    __OBJECT_POINTS_GRID_WORLD_FRAME = np.zeros((__rows * __cols, 3), np.float32)
    __OBJECT_POINTS_GRID_WORLD_FRAME[:, :2] = __BLOCK_SIZE_MM * np.mgrid[0:__rows, 0:__cols].T.reshape(-1, 2)
    __AXIS_XYZ = __BLOCK_SIZE_MM * np.float32([[3, 0, 0], [0, 3, 0], [0, 0, -3]]).reshape(-1, 3)
    __AXIS_CUBE = __BLOCK_SIZE_MM * np.float32([[0, 0, 0], [0, 3, 0], [3, 3, 0], [3, 0, 0],
                       [0, 0, -3], [0, 3, -3], [3, 3, -3], [3, 0, -3]])


    def __init__(self, **kwargs):
        super(ChessBoard, self).__init__(**kwargs)
        self._ret = False


    @classmethod
    def getObjectPoints(cls):
        return cls._ListOfDetectedObjectPoints

    @classmethod
    def getObjectPointsGrid(cls):
        return cls.__OBJECT_POINTS_GRID_WORLD_FRAME

    @classmethod
    def getImagePoints(cls):
        return cls._ListOfDetectedImagePoints

    @classmethod
    def getGrayScaleShape(cls):
        return cls._SHAPE_OF_GRAYSCALE

    def calculateObjectnImagePointsnDisplay(self, drawCorners = True, aggregateToList = True):
        if self._gray is None:
            self.changeToGray()
        ret, corners = openCV.findChessboardCorners(self._gray, (self.__rows, self.__cols), flags=openCV.CALIB_CB_ADAPTIVE_THRESH)

        if ret:
            cornersImproved = openCV.cornerSubPix(self._gray, corners, (11, 11), (-1, -1), self.__criteria)
            self._corners = cornersImproved

            if aggregateToList:
                ChessBoard._ListOfDetectedObjectPoints.append(ChessBoard.__OBJECT_POINTS_GRID_WORLD_FRAME)
                ChessBoard._ListOfDetectedImagePoints.append(cornersImproved)

            if drawCorners:
                imageWithDrawnCorners = np.copy(self._image)
                imageWithDrawnCorners = openCV.drawChessboardCorners(imageWithDrawnCorners, (self.__rows, self.__cols), cornersImproved, ret)
                Utilities.Utils.imshow(imageWithDrawnCorners, waitKey=1000)

        return ret

    @classmethod
    def clearListOfObjectnImagePoints(cls):
        cls._ListOfDetectedImagePoints = []
        cls._ListOfDetectedObjectPoints = []

    def __drawAxesAtOrigin(self, imagePoints):
        if self._corners is None:
            self.calculateObjectnImagePointsnDisplay(drawCorners=False,aggregateToList=False)
        corner = tuple(self._corners[0].ravel())
        image = np.copy(self._image)
        image = openCV.line(self._image, corner, tuple(imagePoints[0].ravel()), (255, 0, 0), 5)
        image = openCV.line(self._image, corner, tuple(imagePoints[1].ravel()), (0, 255, 0), 5)
        image = openCV.line(self._image, corner, tuple(imagePoints[2].ravel()), (0, 0, 255), 5)
        return image

    def drawAxesOnTheChessBoard(self, cameraParams):
        cornersFound = False
        if self._corners is None:
            cornersFound = self.calculateObjectnImagePointsnDisplay(drawCorners=False,aggregateToList=False)

        if cornersFound is False:
            return

        K = cameraParams.getIntrinsicMatrix()
        distortion = cameraParams.getDistortion()
        ret, rvecs, tvecs = openCV.solvePnP(ChessBoard.__OBJECT_POINTS_GRID_WORLD_FRAME, self._corners, K, distortion)
        projectedPointsOnImage, jac = openCV.projectPoints(ChessBoard.__AXIS_XYZ, rvecs, tvecs, K, distortion)
        imageWithAxisDrawn = self.__drawAxesAtOrigin(projectedPointsOnImage)
        Utilities.Utils.imshow(imageWithAxisDrawn, waitKey=2000)

    def findPoseOfPattern(self, cameraParams):
        cornersFound = False
        if self._corners is None:
            cornersFound = self.calculateObjectnImagePointsnDisplay(drawCorners=False, aggregateToList=False)

        if cornersFound is False:
            return None, None

        K = cameraParams.getIntrinsicMatrix()
        distortion = cameraParams.getDistortion()
        ret, rvecs, tvecs = openCV.solvePnP(ChessBoard.__OBJECT_POINTS_GRID_WORLD_FRAME, self._corners, K, distortion)
        return rvecs, tvecs

    def drawCubeOnTheChessBoard(self, cameraParams):
        cornersFound = False
        if self._corners is None:
            cornersFound = self.calculateObjectnImagePointsnDisplay(drawCorners=False,aggregateToList=False)

        if cornersFound is False:
            return
        K = cameraParams.getIntrinsicMatrix()
        distortion = cameraParams.getDistortion()
        ret, rvecs, tvecs = openCV.solvePnP(ChessBoard.__OBJECT_POINTS_GRID_WORLD_FRAME, self._corners, K, distortion)
        projectedPointsOnImage, jac = openCV.projectPoints(ChessBoard.__AXIS_CUBE, rvecs, tvecs, K, distortion)

        projectedPointsOnImage = np.int32(projectedPointsOnImage).reshape(-1, 2)
        image = np.copy(self._image)

        imageWithCubeDrawn = openCV.drawContours(image, [projectedPointsOnImage[:4]], -1, (0, 255, 0), -3)
        for i, j in zip(range(4), range(4, 8)):
            imageWithCubeDrawn = openCV.line(imageWithCubeDrawn, tuple(projectedPointsOnImage[i]), tuple(projectedPointsOnImage[j]), (255), 3)
        imageWithCubeDrawn = openCV.drawContours(imageWithCubeDrawn, [projectedPointsOnImage[4:]], -1, (0, 0, 255), 3)
        Utilities.Utils.imshow(imageWithCubeDrawn, waitKey=2000)

