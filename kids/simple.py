from picamera import PiCamera
from snapchat import *

camera = PiCamera()
camera.resolution = (1024, 768)

output = '/home/pi/image.png'
overlay = 'flowers'

camera.start_preview()
camera.hflip = True
preview_overlay(camera, overlay)
input('Press Enter')
camera.capture(output)
camera.stop_preview()
remove_overlays(camera)
output_overlay(output, overlay)
