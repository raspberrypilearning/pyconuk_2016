from PIL import Image
from glob import glob
from textwrap import dedent

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

def _remove_overlays(camera):
    """
    Remove all overlays from the camera preview
    """
    [camera.remove_overlay(o) for o in camera.overlays]

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

    _remove_overlays(camera)

    overlay_img = _get_overlay_image(overlay)
    pad = Image.new('RGB', (
        ((overlay_img.size[0] + 31) // 32) * 32,
        ((overlay_img.size[1] + 15) // 16) * 16,
    ))
    pad.paste(overlay_img, (0, 0))
    o = camera.add_overlay(pad.tobytes())
    o.alpha = 128
    o.layer = 3

def output_overlay(output=None, overlay=None):
    """
    Given an image overlay and a captured photo, add the overlay to the photo
    and save the new image as a PNG
    """

    if overlay is None or output is None:
        raise ValueError(dedent("""
        Missing argument

        Usage:

        >>> output_overlay(output, overlay)
        """))

    overlay_img = _get_overlay_image(overlay)
    output_img = Image.open(output).convert('RGBA')
    new_output = Image.alpha_composite(output_img, overlay_img)
    new_output.save(output.replace('.jpg', '.png'))

def overlay_gen():
    while True:
        for overlay in overlays:
            yield overlay

all_overlays = overlay_gen()