import numpy as np
import cv2 as cv
import os 

def calibrate(showPics=True):
    # Update the image path
    calibrationDir = '/home/pi/Desktop'
    imgPathList = [os.path.join(calibrationDir, 'aruco.png')]

    # Initialize  
    nRows = 6 
    nCols = 6 
    termCriteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    worldPtsCur = np.zeros((nRows * nCols, 3), np.float32)
    worldPtsCur[:, :2] = np.mgrid[0:nRows, 0:nCols].T.reshape(-1, 2)
    worldPtsList = []
    imgPtsList = [] 

    # Find Corners 
    for curImgPath in imgPathList:
        imgBGR = cv.imread(curImgPath)
        imgGray = cv.cvtColor(imgBGR, cv.COLOR_BGR2GRAY)
        cornersFound, cornersOrg = cv.findChessboardCorners(imgGray, (nRows, nCols), None)

        if cornersFound == True:
            worldPtsList.append(worldPtsCur)
            cornersRefined = cv.cornerSubPix(imgGray, cornersOrg, (11, 11), (-1, -1), termCriteria)
            imgPtsList.append(cornersRefined)

            if showPics: 
                cv.drawChessboardCorners(imgBGR, (nRows, nCols), cornersRefined, cornersFound)
                cv.imshow('Chessboard', imgBGR)
                cv.waitKey(500)
    cv.destroyAllWindows()

    # Calibrate 
    repError, camMatrix, distCoeff, rvecs, tvecs = cv.calibrateCamera(
        worldPtsList, imgPtsList, imgGray.shape[::-1], None, None)
    print('Camera Matrix:\n', camMatrix)
    print("Reproj Error (pixels): {:.4f}".format(repError))
    
    # Save Calibration Parameters (later video)
    paramPath = os.path.join(calibrationDir, 'calibration.npz')
    np.savez(paramPath, 
            repError=repError, 
            camMatrix=camMatrix, 
            distCoeff=distCoeff, 
            rvecs=rvecs, 
            tvecs=tvecs)
    
    return camMatrix, distCoeff

def removeDistortion(camMatrix, distCoeff): 
    # Update the image path for distortion removal demonstration
    imgPath = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/aruco/aruco.jpg'
    img = cv.imread(imgPath)
    
    height, width = img.shape[:2]
    camMatrixNew, roi = cv.getOptimalNewCameraMatrix(camMatrix, distCoeff, (width, height), 1, (width, height)) 
    imgUndist = cv.undistort(img, camMatrix, distCoeff, None, camMatrixNew)

    # Draw Line to See Distortion Change 
    cv.line(img, (1769, 103), (1780, 922), (255, 255, 255), 2)
    cv.line(imgUndist, (1769, 103), (1780, 922), (255, 255, 255), 2)

    # Display images
    cv.imshow('Original Image', img)
    cv.imshow('Undistorted Image', imgUndist)
    cv.waitKey(0)
    cv.destroyAllWindows()

def runCalibration(): 
    calibrate(showPics=True)
   
def runRemoveDistortion(): 
    camMatrix, distCoeff = calibrate(showPics=False) 
    removeDistortion(camMatrix, distCoeff) 

if __name__ == '__main__':
    # runCalibration() 
    runRemoveDistortion() 
