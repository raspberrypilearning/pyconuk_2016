from picamera import PiCamera
from gpiozero import Button
from snapchat import *
from time import sleep

output = '/home/pi/photo.jpg'
overlay = 'flowers'

camera = PiCamera()
left = Button(20)
right = Button(21)

def next_overlay():
    global overlay
    overlay = next(all_overlays)
    preview_overlay(camera, overlay)

left.when_pressed = next_overlay

camera.start_preview()
camera.hflip = True
preview_overlay(camera, overlay)
right.wait_for_press()
#sleep(5)
camera.capture(output)
output_overlay(output, overlay)

camera.close()
