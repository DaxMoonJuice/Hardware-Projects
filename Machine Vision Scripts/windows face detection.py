# import the necessary packages
#!/usr/bin/env python


import time
import numpy as np
import cv2


face_cascade=cv2.CascadeClassifier('C:/Users/Joshes Computer/Documents/opencv/build/etc/haarcascades/haarcascade_frontalface_alt.xml')
print face_cascade
# initialize the camera and grab a reference to the raw camera capture


cap= cv2.VideoCapture(0)


#vs =PiVideoStream().start() 
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
# this is the pi-camera method for looping through video stream
while (True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        
        
        ret,image = cap.read()
        
        #Face Detection--1.Convert Image to Greyscale so Haar cascade works
        gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        #creates the face object
        faces = face_cascade.detectMultiScale(gray, 1.5,5)
        print ("Found"+str(len(faces))+" faces")
        #for each face in faces draw a rectangle with dimensions w+h at the face co-rd x+y
        
        for (x,y,w,h) in faces:
                cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)
                #print w
                #print h
                
                s_img=cv2.imread('C:/Users/Joshes Computer/Documents/Hacking Folder/Retro VR googles/Machine Vision Scripts/smileyface.jpg')
                s_img=cv2.cvtColor(s_img, cv2.COLOR_BGR2GRAY)

                dim=(w,h)
                
                s_img= cv2.resize(s_img, dim, interpolation =cv2.INTER_AREA)
                c1=y
                r1=x
                offset1=s_img.shape[0]
                gray[c1:c1+offset1,r1:r1+offset1]=s_img
                #cv2.imwrite("test.jpg",gray)
                x_offset=x+w
                y_offset=y+h
                

                
                offsetx=s_img.shape[0]
                offsety=s_img.shape[1]
                #gray[0:50,0:50]
                #gray[w:offsety,h:offsety]=s_img                                           
 
        # show the frame
        cv2.imshow("Frame", gray)
        #stores the value of a the last keypress?
        key = cv2.waitKey(1) & 0xFF
 
        # clear the stream in preparation for the next frame
        
 
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break


cap.release
cv2.destroyAllWindows()
