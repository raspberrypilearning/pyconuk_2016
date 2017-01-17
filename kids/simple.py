from picamera import PiCamera
from gpiozero import Button
from snapchat import *
from time import sleep

camera = PiCamera()
button = Button(16)

output = '/home/pi/image.jpg'
overlay = 'flowers'

camera.start_preview()
camera.hflip = True
preview_overlay(camera, overlay)
button.wait_for_press()
sleep(3)
camera.capture(output)
camera.stop_preview()
remove_overlays(camera)
output_overlay(output, overlay)
