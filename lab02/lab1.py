#!/usr/bin/env python3

import math

from PIL import Image as Image

# NO ADDITIONAL IMPORTS ALLOWED!


def get_pixel(image, x, y):
    # Adjust edge effects
    x = 0 if x < 0 else x
    x = image['width'] - 1 if x >= image['width'] else x
    y = 0 if y < 0 else y
    y = image['height'] - 1 if y >= image['height'] else y
    return image['pixels'][x + y*image['width']]


def set_pixel(image, x, y, c):
    image['pixels'][x + y*image['width']] = c


def apply_per_pixel(image, func):
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [0] * image['height'] * image['width'],
    }
    for x in range(image['width']):
        for y in range(image['height']):
            color = get_pixel(image, x, y)
            newcolor = func(color)
            set_pixel(result, x, y, newcolor)
    return result


def inverted(image):
    return apply_per_pixel(image, lambda c: 255-c)


# HELPER FUNCTIONS

def get_kernel(kernel, x, y):
    """
    Returns the kernel value at kernel[x, y].
    """
    return kernel['flat_kernel'][x + y*kernel['size']]

def get_correlation(image, x, y, kernel):
    """
    Computes and returns the correlated pixel at image pixel (x,y) based on the
    correlation kernel.
    """
    n = kernel['size']
    newcolor = 0
    mid = n // 2
    for x_kernel in range(n):
        for y_kernel in range(n):
            x_image = x - mid + x_kernel
            y_image = y - mid + y_kernel
            color = get_pixel(image, x_image , y_image)
            kernel_value = get_kernel(kernel, x_kernel, y_kernel)
            newcolor += color * kernel_value
    return newcolor

def correlate(image, kernel):
    """
    Compute the result of correlating the given image with the given kernel.

    The output of this function should have the same form as a 6.009 image (a
    dictionary with 'height', 'width', and 'pixels' keys), but its pixel values
    do not necessarily need to be in the range [0,255], nor do they need to be
    integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    The kernel is a dictionary similar to the image dictionary.
    kernel = {'size': n, flat_kernel: []}
    The kernel['flat_kernel'] stores the nxn kernel matrix in row-major order.
    """
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [0] * image['height'] * image['width'],
    }
    for x in range(image['width']):
        for y in range(image['height']):
            newcolor = get_correlation(image, x, y, kernel)
            set_pixel(result, x, y, newcolor)
    return result


def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the 'pixels' list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    pixels = image['pixels']
    for i, pixel in enumerate(pixels):
        pixels[i] = 0 if pixel < 0 else (255 if pixel > 255 else round(pixel))

# FILTERS

def get_boxblur(n):
    """
    Returns a nxn boxblur kernel.
    """
    return {
        'size': n,
        'flat_kernel': [1/n ** 2] * n ** 2
    }

def blurred(image, n):
    """
    Return a new image representing the result of applying a box blur (with
    kernel size n) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    # first, create a representation for the appropriate n-by-n kernel (you may
    # wish to define another helper function for this)
    boxblur = get_boxblur(n)

    # then compute the correlation of the input image with that kernel
    result = correlate(image, boxblur)

    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.
    round_and_clip_image(result)

    return result

def get_sharpkernel(n):
    """
    Returns a nxn sharp kernel of the form 2I - B
    """
    kernel =  {
        'size': n,
        'flat_kernel': [-1/n ** 2] * n ** 2
    }
    kernel['flat_kernel'][n ** 2 // 2] += 2

    return kernel

def sharpened(image, n):
    """
    Return a new image representing the result of applying an unshparp mask
    of blurred kernel size n to the given input image.

    S = 2I - B

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    sharpkernel = get_sharpkernel(n)

    result = correlate(image, sharpkernel)

    round_and_clip_image(result)

    return result

def edges(image):
    """
    Return a new image representing the result of sobel operator for edge
    detection. Both a Kx and Ky correlation is performed. Each of 3x3.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    kernel_x = {'size': 3, 'flat_kernel': [-1, 0, 1, -2, 0, 2, -1, 0, 1]}
    result_x = correlate(image, kernel_x)
    kernel_y = {'size': 3, 'flat_kernel': [-1, -2, -1, 0, 0, 0, 1, 2, 1]}
    result_y = correlate(image, kernel_y)

    result = { 
        'width': image['width'],
        'height': image['height'],    
    }

    result["pixels"] = list(map(lambda x, y: math.sqrt(x**2 + y**2),
     result_x['pixels'], result_y['pixels']))
    
    round_and_clip_image(result)

    return result

# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES

def load_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_image('test_images/cat.png')
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


def save_image(image, filename, mode='PNG'):
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
    import os
    TEST_DIRECTORY = os.path.dirname(__file__)
    im = load_image(os.path.join(TEST_DIRECTORY, 'test_images', 'bluegill.png'))
    kernel_x = {'size': 3, 'flat_kernel': [-1, 0, 1, -2, 0, 2, -1, 0, 1]}
    result_x = correlate(im, kernel_x)
    kernel_y = {'size': 3, 'flat_kernel': [-1, -2, -1, 0, 0, 0, 1, 2, 1]}
    result_y = correlate(im, kernel_y)
    save_image(result_x, 'output_x.png')
    save_image(result_y, 'output_y.png')