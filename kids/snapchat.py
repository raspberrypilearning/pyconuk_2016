import io
import os
import datetime as dt
from itertools import cycle
from signal import pause
from picamera import PiCamera
from gpiozero import Button
from PIL import Image, ImageFont, ImageDraw

camera = None             # the camera
overlay = None            # the overlay renderer
overlay_images = None     # infinite iterator of overlay images
overlay_image = None      # the current overlay image
overlay_offset = 0        # vertical offset of the overlay image
overlay_caption = ''      # string to draw over image
font = None               # the font used for captions

def main():
    global camera, overlay, overlay_images, font

    # Load the font that we're going to use in our overlays
    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/roboto/Roboto-Regular.ttf", 48)
    # Load all the overlay images and make an infinite cycle
    # of them
    overlays_path = os.path.join(os.path.dirname(__file__), 'overlays')
    overlay_images = [
        Image.open(os.path.join(overlays_path, filename))
        for filename in os.listdir(overlays_path)
        if filename.endswith('.png')
        ]
    overlay_images = iter(cycle(overlay_images))
    # Use a 4:3 resolution or you'll wind up with offset problems
    camera = PiCamera(resolution='1024x768', framerate=30)
    camera.start_preview()
    # Create an initially blank overlay with the same resolution as
    # the camera
    blank = Image.new('RGB', pad(camera.resolution))
    overlay = camera.add_overlay(
        blank.tobytes(), size=camera.resolution, alpha=128, layer=3)
    next_overlay()
    # Set up the buttons
    next_overlay_btn = Button(15)
    next_overlay_btn.when_pressed = next_overlay
    capture_btn = Button(24)
    capture_btn.when_pressed = take_picture
    up_btn = Button(7, hold_time=1/camera.framerate, hold_repeat=True)
    up_btn.when_pressed = move_overlay_up
    up_btn.when_held = move_overlay_up
    down_btn = Button(20, hold_time=1/camera.framerate, hold_repeat=True)
    down_btn.when_pressed = move_overlay_down
    down_btn.when_held = move_overlay_down
    # Wait around for the event handlers to do things
    pause()

def next_overlay():
    global overlay_image
    overlay_image = next(overlay_images)
    update_overlay()

def move_overlay_up():
    global overlay_offset
    overlay_offset = min(camera.resolution[1], max(0, overlay_offset - 1))
    update_overlay()

def move_overlay_down():
    global overlay_offset
    overlay_offset = min(camera.resolution[1], max(0, overlay_offset + 1))
    update_overlay()

def update_overlay():
    # pad out the image to the camera's resolution, placing it in the
    # horizontal center, with the vertical position determined by
    # overlay_offset
    img = Image.new('RGB', pad(camera.resolution))
    x = camera.resolution[0] // 2 - overlay_image.size[0] // 2
    y = overlay_offset
    img.paste(overlay_image, (x, y), mask=overlay_image)
    overlay.update(img.tobytes())

def take_picture():
    # Take a picture and open it as a PIL Image
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg')
    stream.seek(0)
    output = Image.open(stream).convert('RGBA')
    # Draw the selected overlay over the captured image
    x = camera.resolution[0] // 2 - overlay_image.size[0] // 2
    y = overlay_offset
    output.paste(overlay_image, (x, y), mask=overlay_image)
    # If a caption has been set, draw that too
    if overlay_caption:
        draw = ImageDraw.Draw(output)
        width, height = font.getsize(overlay_caption)
        left = camera.resolution[0] // 2 - width // 2
        top = camera.resolution[1] // 2 - height // 2
        right = left + width
        bottom = top + height
        draw.rectangle((left, top, right, bottom), fill=(0, 0, 0))
        draw.text((left, top), overlay_caption, (255, 255, 255), font=font)
    output.save('/home/pi/snapchat-{now:%d-%m-%H-%M-%S}.jpg'.format(
        now=dt.datetime.now()))

def pad(resolution, width=32, height=16):
    # A little utility routine which pads the specified resolution
    # up to the nearest multiple of *width* and *height*; this is
    # needed because overlays require padding to the camera's
    # block size (32x16)
    return (
        ((resolution[0] + (width - 1)) // width) * width,
        ((resolution[1] + (height - 1)) // height) * height,
        )


main()
