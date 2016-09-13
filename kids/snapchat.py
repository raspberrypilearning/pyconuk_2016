from PIL import Image, ImageFont, ImageDraw
from glob import glob
from textwrap import dedent
from time import gmtime, strftime

overlays_dir = '/home/pi/overlays'
overlays = [
    img.split('/')[-1].split('.')[0]
    for img in glob('{}/*'.format(overlays_dir))
]

def _get_overlay_image(overlay):
    """
    Given the name of an overlay (without file extension), return the
    corresponding Image object
    """
    return Image.open('{}/{}.png'.format(overlays_dir, overlay))

def _overlay_gen():
    """
    Returns an infinite generator cycling over each overlay
    """
    while True:
        for overlay in overlays:
            yield overlay

def remove_overlays(camera):
    """
    Remove all overlays from the camera preview
    """
    [camera.remove_overlay(o) for o in camera.overlays]

def gen_filename():
    """
    Generates a filename with a timestamp
    """
    filename = strftime("/home/pi/snapchat-%d-%m %H:%M.png", gmtime())
    return filename


def preview_overlay(camera=None, overlay=None):
    """
    Given the PiCamera object and an image overlay, add the overlay to the
    camera preview
    """

    if camera is None or overlay is None:
        raise ValueError(dedent("""
        Missing argument

        Usage:

        >>> preview_overlay(camera, overlay)
        """))

    if overlay not in overlays:
        raise ValueError(dedent("""
        Overlay not available

        Available overlays: {}
        """.format(', '.join(o for o in overlays))))

    remove_overlays(camera)

    overlay_img = _get_overlay_image(overlay)
    pad = Image.new('RGB', (
        ((overlay_img.size[0] + 31) // 32) * 32,
        ((overlay_img.size[1] + 15) // 16) * 16,
    ))
    pad.paste(overlay_img, (0, 0))
    o = camera.add_overlay(pad.tobytes())
    o.alpha = 128
    o.layer = 3

def output_overlay(output=None, overlay=None, caption=""):
    """
    Given an image overlay and a captured photo, add the overlay to the photo
    and save the new image in its place
    """

    if overlay is None or output is None:
        raise ValueError(dedent("""
        Missing argument

        Usage:

        >>> output_overlay(output, overlay)

        or:

        >>> output_overlay(output, overlay, caption)
        """))

    overlay_img = _get_overlay_image(overlay)
    output_img = Image.open(output).convert('RGBA')
    new_output = Image.alpha_composite(output_img, overlay_img)
    draw = ImageDraw.Draw(new_output)
    font = ImageFont.truetype("/usr/share/fonts/truetype/roboto/Roboto-Regular.ttf", 48)
    w, h = font.getsize(caption)
    x1 = (1366 - w) / 2
    x2 = x1 + w
    y1 = 768 - h
    y2 = 768 - h
    draw.rectangle((x1, y1, x2, y2), fill="black")
    draw.text((x1, y1), caption,(255, 255, 255), font=font)
    new_output.save(output.replace('.jpg', '.png'))

all_overlays = _overlay_gen()
