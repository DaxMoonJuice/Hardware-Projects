# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
#Modded for face recognition in a video stream
#Import face_cascade

face_cascade=cv2.CascadeClassifier('haarcascade_frontface_default.xml')
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	#Image is now an array of values from the current frame
	image = frame.array

	#Face Detection--1.Convert Image to Greyscale so Haar cascade works
	gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	#creates the face object
	faces = face_cascade.detectMultiScale(gray, 1.3,5)
	#for each face in faces draw a rectangle with dimensions w+h at the face co-rd x+y
	for (x,y,w,h) in faces:
            image = cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]
 
	# show the frame
	cv2.imshow("Frame", image)
        #stores the value of a the last keypress?
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
