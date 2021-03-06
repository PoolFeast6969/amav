# import the necessary packages
from imutils.video import VideoStream
import datetime
import argparse
import imutils
import time
import cv2
import numpy as np
import zbar
from PIL import Image

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())


# initialize the video stream and allow the cammera sensor to warmup
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

#
#faceCascade = cv2.CascadeClassifier("~/opencv-2.4.10/data/haarcascades/haarcascade_frontalface_default.xml")
#faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
scanner = zbar.ImageScanner()
scanner.parse_config('enable')
# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	#image noise reduction reduce number of false circles detected
	blur = cv2.GaussianBlur(gray,(5,5),0)
	# detect circles in the image
	circles = cv2.HoughCircles(blur, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 200)

	# draw the timestamp on the frame
	timestamp = datetime.datetime.now()
	ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
	cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
	
	if circles is not None:
		# convert the (x, y) coordinates and radius of the circles to integers
		circles = np.round(circles[0, :]).astype("int")

		# loop over the (x, y) coordinates and radius of the circles
		for (x, y, r) in circles:
			# draw the circle in the output image, then draw a rectangle
			# corresponding to the center of the circle
			cv2.circle(frame, (x, y), r, (0, 255, 0), 1)
			cv2.rectangle(frame, (x - 1, y - 1), (x + 1, y + 1), (0, 128, 255), -1)
	
	
	# show the frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
