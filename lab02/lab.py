#!/usr/bin/env python3

# NO ADDITIONAL IMPORTS!
# (except in the last part of the lab; see the lab writeup for details)
import math
from PIL import Image
import lab1


# CODE FROM LAB 1 (replace with your code)

def inverted(image):
    return lab1.inverted(image)


def correlate(image, kernel):
    return lab1.correlate(image, kernel)


def round_and_clip_image(image):
    return lab1.round_and_clip_image(image)


def blurred(image, n):
    return lab1.blurred(image, n)


def sharpened(image, n):
    return lab1.sharpened(image, n)


def edges(image):
    return lab1.edges(image)

# LAB 2 FILTERS


def extract_rgb(image):
    """
    Given an r, g, b image, returns a tuple of single color
    images. Each similar to a greyscale image
    """
    r = {
        'height': image['height'],
        'width': image['width'],
        'pixels': []
    }

    g = {
        'height': image['height'],
        'width': image['width'],
        'pixels': []
    }

    b = {
        'height': image['height'],
        'width': image['width'],
        'pixels': []
    }

    for pixel_r, pixel_g, pixel_b in image['pixels']:
        r['pixels'].append(pixel_r)
        g['pixels'].append(pixel_g)
        b['pixels'].append(pixel_b)

    return r, g, b


def make_rgb(red_image, green_image, blue_image):
    """
    Given images representing the red, green, and blue channels of the
    same image, returns the composition of them into a single colored
    image.
    """
    image = {
        'height': red_image['height'],
        'width': red_image['width']
    }

    image['pixels'] = [(r, g, b) for r, g, b in
                       zip(red_image['pixels'], green_image['pixels'], blue_image['pixels'])]

    return image


def color_filter_from_greyscale_filter(filt):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """
    def color_filter(image):
        red_image, green_image, blue_image = extract_rgb(image)
        filtered_images = []
        for source_image in [red_image, green_image, blue_image]:
            filtered_images.append(filt(source_image))

        new_color_image = make_rgb(*filtered_images)
        return new_color_image

    return color_filter


def make_blur_filter(n):
    """
    Given a size n, returns a blur filter function of kernel size
    n x n.
    """
    def blur_filter(image):
        return blurred(image, n)
    return blur_filter


def make_sharpen_filter(n):
    """
    Given a size n, returns a sharpen filter function of kernel size
    n x n.
    """
    def sharpen_filter(image):
        return sharpened(image, n)
    return sharpen_filter


def filter_cascade(filters):
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """
    def apply_filters(image):
        new_img = image.copy()
        for filter in filters:
            new_img = filter(new_img)
        return new_img
    return apply_filters


# SEAM CARVING

# Main Seam Carving Implementation

def seam_carving(image, ncols):
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image.
    """
    new_img = {
        'width': image['width'],
        'height': image['height'],
        'pixels': image['pixels'][:]
    }
    for _ in range(ncols):
        seam = minimum_energy_seam(
            cumulative_energy_map(
                compute_energy(
                    greyscale_image_from_color_image(new_img))))
        new_img = image_without_seam(new_img, seam)

    return new_img


# Optional Helper Functions for Seam Carving

def greyscale_image_from_color_image(image):
    """
    Given a color image, computes and returns a corresponding greyscale image.

    Returns a greyscale image (represented as a dictionary).
    """
    greyscale_pixels = [round(.299*r + .587*g + .114*b)
                        for r, g, b in image['pixels']]
    return {
        'height': image['height'],
        'width': image['width'],
        'pixels': greyscale_pixels
    }


def compute_energy(grey):
    """
    Given a greyscale image, computes a measure of "energy", in our case using
    the edges function from last week.

    Returns a greyscale image (represented as a dictionary).
    """
    return edges(grey)


def cumulative_energy_map(energy):
    """
    Given a measure of energy (e.g., the output of the compute_energy
    function), computes a "cumulative energy map" as described in the lab 2
    writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys (but where
    the values in the 'pixels' array may not necessarily be in the range [0,
    255].
    """
    width = energy['width']
    height = energy['height']
    cem = {
        'width': width,
        'height': height,
        'pixels': energy['pixels'][:]
    }

    # Left top row untouched
    for y in range(1, height):
        for x in range(width):
            current_value = lab1.get_pixel(cem, x, y)
            adjacent_pixels = [lab1.get_pixel(
                cem, x - i, y - 1) for i in [-1, 0, 1]]
            lab1.set_pixel(cem, x, y, current_value + min(adjacent_pixels))

    return cem


def get_flat_index(x, y, width):
    """
    Given indices (x, y) of a matrix of size width x height, returns the
    corresponding index of the flattened array in row-major order.
    """
    return y*width + x


def minimum_energy_seam(cem):
    """
    Given a cumulative energy map, returns a list of the indices into the
    'pixels' list that correspond to pixels contained in the minimum-energy
    seam (computed as described in the lab 2 writeup).
    """
    remove_indices = []
    width = cem['width']
    height = cem['height']
    cem_pixels = cem['pixels']

    # Get bottom of min seam
    bottom: list = cem_pixels[-width:]
    x_bottom = bottom.index(min(bottom))
    remove_indices.append(get_flat_index(x_bottom, height - 1, width))

    x_min = x_bottom
    for y in reversed(range(height - 1)):
        # Get (x, value) array of adjacent pixels on row
        adjacent_pixels = [(x_min + i, lab1.get_pixel(cem, x_min + i, y))
                           for i in [-1, 0, 1]]
        (x_min, _) = min(adjacent_pixels, key=lambda x: x[1])
        # Crop x_min between 0 and width - 1
        x_min = min(max(0, x_min), width - 1)
        remove_indices.append(get_flat_index(x_min, y, width))

    return remove_indices


def image_without_seam(image, seam):
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """
    pixels = image['pixels']
    new_pixels = []
    for i in range(len(pixels)):
        if i not in seam:
            new_pixels.append(pixels[i])

    return {
        'width': image['width'] - 1,
        'height': image['height'],
        'pixels': new_pixels
    }


# HELPER FUNCTIONS FOR LOADING AND SAVING COLOR IMAGES

def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img = img.convert('RGB')  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_color_image(image, filename, mode='PNG'):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode='RGB', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns an instance of this class
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith('RGB'):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == 'LA':
            pixels = [p[0] for p in img_data]
        elif img.mode == 'L':
            pixels = list(img_data)
        else:
            raise ValueError('Unsupported image mode: %r' % img.mode)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_greyscale_image(image, filename, mode='PNG'):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode='L', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    cem = {'width': 9, 'height': 4, 'pixels': [160, 160, 0, 28, 0, 28, 0, 160, 160, 415, 218, 10, 22, 14,
                                               22, 10, 218, 415, 473, 265, 40, 10, 28, 10, 40, 265, 473, 520, 295, 41, 32, 10, 32, 41, 295, 520]}
    print(minimum_energy_seam(cem))
