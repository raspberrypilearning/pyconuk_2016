from picamera import PiCamera
from gpiozero import Button
from snapchat import *
from time import sleep

camera = PiCamera()
left = Button(16)
right = Button(12)

while True:
    output = gen_filename()
    overlay = 'flowers'

    def next_overlay():
        global overlay
        overlay = next(all_overlays)
        preview_overlay(camera, overlay)

    left.when_pressed = next_overlay

    camera.start_preview()
    camera.hflip = True
    preview_overlay(camera, overlay)
    right.wait_for_press()
    sleep(3)
    camera.capture(output)
    camera.stop_preview()
    remove_overlays(camera)
    caption = input("Enter a caption for your image: ")
    output_overlay(output, overlay,caption)
