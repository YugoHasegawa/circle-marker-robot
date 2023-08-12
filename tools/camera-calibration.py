import numpy as np
import cv2
import glob

board_size = (8,6)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(7,5,0)
objp = np.zeros((board_size[0]*board_size[1],3), np.float32)
objp[:,:2] = np.mgrid[0:board_size[0],0:board_size[1]].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# prepare camera
cap = cv2.VideoCapture(0)

filenames = glob.glob('images/*.jpg')

lastfilename = None
for filename in filenames:
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, board_size)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        imgpoints.append(corners)

        cv2.drawChessboardCorners(img, board_size, corners, ret)
        cv2.imshow('img',img)
        cv2.waitKey(500)
        lastfilename = filename

img = cv2.imread(lastfilename)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
rms, mtx, dist, _, _ = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
print(f"RMS:{rms}")
print(f"mtx:{mtx}")
print(f"dist:{dist}")

undistorted_img = cv2.undistort(img, mtx, dist)
cv2.imshow("undistored", undistorted_img)
cv2.waitKey()

cap.release()
cv2.destroyAllWindows()
