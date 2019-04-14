from SimpleCV import Camera,Display, Image

cam = Camera()
display=Display()

#while True
img = cam.getImage()
img.show()
