#!/bin/python

# Draw a repeated SVG pattern based on a boolean matrix
# 28" x 146"
# have somewhere between 80 and 90 pixels to work with based on the smallest_bool matrix.

import numpy as np

CIRCLE = """<circle cx="{x}" cy="{y}" r="{radius}" fill="url(#gradient)" transform="rotate({rot})" />"""
ELLIPSE = """<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="url(#gradient)" transform="rotate{rot})" />"""

TEARDROP = '<use x="0" y="0" xlink:href="#tear" transform="translate({x} {y}) rotate({rot})"/>'
BASE_HTML = """<?xml version="1.0" encoding="UTF-8"?>

<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
    <linearGradient id="gradient">
        <stop offset="20%" stop-color="red" />
	<stop offset="90%" stop-color="blue" />
    </linearGradient>
    <g id="tear">
	<path fill="url(#gradient)" stroke="#000" stroke-width="1.5"
		d="M15 3
		   Q16.5 6.8 25 18
		   A12.8 12.8 0 1 1 5 18
		   Q13.5 6.8 15 3z" />
    </g>
</defs>
{code}
</svg>
"""


def main(boolean_array, node_resolution=25, output_file="tears.svg"):
    '''Draw svg pattern based on an array of booleans

False will mean the pattern doesn't exist, True will mean it does.

:param boolean_array: Array of booleans on which to base the knot.
:type boolean_array: `numpy.ndarray`'''


    orig_shape = boolean_array.shape
    image_dimensions = [x * node_resolution for x in orig_shape]
    out_str = []  # open(output_file, "w")  # Create an array surrounded by zeros so the rotation math is easy.
    X, Y = boolean_array.shape
    padded_array = np.zeros((X + 2, Y + 2))
    padded_array[1:-1, 1:-1] = boolean_array  # Write nodes in for all True values
    for y in range(orig_shape[1]):
        for x in range(orig_shape[0]):
            if boolean_array[x, y]:
                out_str.append(TEARDROP.format(x=x * node_resolution,
                                               y=y * node_resolution,
                                               rot=get_rot(padded_array, x+1, y+1)))
    with open(output_file, "w") as f:
        f.writelines(BASE_HTML.format(width=image_dimensions[0], height=image_dimensions[1], code="\n".join(out_str)))

def main_circle(boolean_array, node_resolution=5, output_file="circles.svg"):
    orig_shape = boolean_array.shape
    image_dimensions = [x * node_resolution for x in orig_shape]
    out_str = []  # open(output_file, "w")  # Create an array surrounded by zeros so the rotation math is easy.
    X, Y = boolean_array.shape
    padded_array = np.zeros((X + 2, Y + 2))
    padded_array[1:-1, 1:-1] = boolean_array  # Write nodes in for all True values
    for y in range(orig_shape[1]):
        for x in range(orig_shape[0]):
            if boolean_array[x, y]:
                out_str.append(CIRCLE.format(x=x * node_resolution,
                                             y=y * node_resolution,
                                             radius=node_resolution / 2,
                                             rot=get_rot(padded_array, x+1, y+1)))
    with open(output_file, "w") as f:
        f.writelines(BASE_HTML.format(width=image_dimensions[0], height=image_dimensions[1], code="\n".join(out_str)))



def get_rot(boolean_array, x, y):
    '''Determine angle of shape based on surrounding boolean matrix'''
    angle_array = np.array([[315, 0, 45], [270, 0, 90], [225, 180, 135]])
    local_array = boolean_array[x - 1:x + 2, y - 1:y + 2]
    return (angle_array * local_array).sum() / local_array.sum() + 90


if __name__ == "__main__":
    boolean_array = np.load('smallest_bool_matrix.npy').T
    N = 1
    for i in range(N):
        section = int(boolean_array.shape[1] / N)
        main(boolean_array[:, (i * section):((i + 1) * section)], node_resolution=25, output_file="tears.svg")
