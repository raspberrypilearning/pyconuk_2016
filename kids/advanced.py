from picamera import PiCamera
from gpiozero import Button
from snapchat import *
from time import sleep

camera = PiCamera()
camera.resolution = (1024, 768)

left = Button(20)
right = Button(21)

output = gen_filename()

def next_overlay():
    global overlay
    overlay = next(all_overlays)
    preview_overlay(camera, overlay)

left.when_pressed = next_overlay

camera.start_preview()
camera.hflip = True
right.wait_for_press()
sleep(1)
camera.capture(output)
camera.stop_preview()
remove_overlays(camera)
caption = input("Enter a caption for your image: ")
output_overlay(output, overlay, caption)
