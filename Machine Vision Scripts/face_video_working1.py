# import the necessary packages
#!/usr/bin/env python

from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2

#Modded for face recognition in a video stream
#Import face_cascade
#s_img=cv2.imread("lena.jpg")
#s_img=cv2.cvtColor(s_img, cv2.COLOR_BGR2GRAY)
face_cascade=cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
#vs =PiVideoStream().start() 
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
# this is the pi-camera method for looping through video stream
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	#Image is now an array of values from the current frame
#	image=vs.read()
#	frame=imutils.resize(frame,width=400)	
	image = frame.array
	#Face Detection--1.Convert Image to Greyscale so Haar cascade works
	gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	#creates the face object
	faces = face_cascade.detectMultiScale(gray, 1.5,5)
	print "Found"+str(len(faces))+ " faces"
	#for each face in faces draw a rectangle with dimensions w+h at the face co-rd x+y
	
	for (x,y,w,h) in faces:
		cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)
		#print w
		#print h
		
		s_img=cv2.imread("smileyface.jpg")
		s_img=cv2.cvtColor(s_img, cv2.COLOR_BGR2GRAY)

		dim=(w,h)
		print dim
		#dim=(50,50)
	#	r= 120/s_img.shape[1]	
	#	dim = (120, int(s_img.shape[0] *r))
		s_img= cv2.resize(s_img, dim, interpolation =cv2.INTER_AREA)
		print x
		print y
		print w
		print h
		c1=y
                r1=x
		offset1=s_img.shape[0]
                gray[c1:c1+offset1,r1:r1+offset1]=s_img
		#cv2.imwrite("test.jpg",gray)
		x_offset=x+w
		y_offset=y+h
		print s_img.shape
		#print"x offset"
		print x_offset
		#print"y offset"
		print y_offset
		#print "grey dimensions"
		#print gray.shape
		#x_offset=y_offset=50
		#gray[y_offset:y_offset+s_img.shape[0],x_offset:x_offset+s_img.shape[1]] =s_img
		#gray[x:w,y:h]=s_img
		#size of insert needs to match canvas
		offsetx=s_img.shape[0]
		offsety=s_img.shape[1]
		#gray[0:50,0:50]
		#gray[w:offsety,h:offsety]=s_img				           
 
	# show the frame
	cv2.imshow("Frame", gray)
        #stores the value of a the last keypress?
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break



