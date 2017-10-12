#!/bin/python

#Draw celtic knots based on a boolean array

import numpy as np

STYLE_TEXT = """
    <style>
        <colors>
            <color alpha="255">#ac3030</color>
            <color alpha="255">#34598c</color>
            <color alpha="255">#526105</color>
        </colors>
        <borders>
            <border width="1" alpha="255">#fffffe</border>
        </borders>
        <cusp>
            <shape>round</shape>
            <angle>360</angle>
            <distance>0</distance>
            <curve>24</curve>
        </cusp>
        <crossing>
            <gap>{gap}</gap>
            <slide>{slide}</slide>
            <curve>24</curve>
        </crossing>
        <stroke>
            <width>{width}</width>
            <style>SolidPattern</style>
            <join>RoundJoin</join>
        </stroke>
    </style>"""

def main(boolean_array, node_resolution=20, output_file="boolean.knot"):
	'''Draw celtic knots based on an array of booleans
cf. http://www.cs.columbia.edu/~cs6204/files/Lec7,8a-CelticKnots.pdf

False will mean a knot barrier.  True will mean the knot continues.

Barriers can be vertical or horizontal. As this algorithm is designed for a runner
carpet, I'm going to start with every barrier being vertical.

I can use a cpp program called Knotter to turn properly-formatted XML into a celtic knot. So all I have to do is translate the boolean array into a series of nodes and edges.In knotter format, nodes must be connected to each other.

:param boolean_array: Array of booleans on which to base the knot.
:type boolean_array: `numpy.ndarray`'''
	orig_shape = boolean_array.shape
	image_dimensions = [x*node_resolution for x in orig_shape]
	out_str = []#open(output_file, "w")
	out_str.append('<?xml version="1.0" encoding="UTF-8"?>')
	out_str.append('<knot version="4" generator="Knotter 0.9.7_devel">')
	#out_str.append(STYLE_TEXT.format(distance=node_resolution/2, width=node_resolution/2, gap=int(node_resolution * 9./20), slide=(node_resolution * (0.5/20))))
	out_str.append(STYLE_TEXT.format(distance=0, width=5, gap=9, slide=0.5))
	out_str.append("\t<graph>")
	out_str.append("\t\t<nodes>")

	#Write nodes in for all True values
	base_x = -image_dimensions[0] / 2
	base_y = -image_dimensions[1] / 2
	NODE_TEMPLATE = '\t\t\t<node id="node_{}" x="{}" y="{}"/>'
	EDGE_TEMPLATE = '\t\t\t<edge type="regular" v1="node_{}" v2="node_{}"/>'
	node_str = []
	edge_str = []
	for y in range(orig_shape[1]):
		for x in range(orig_shape[0]):
			if boolean_array[x,y]:
				n_id = x + y*orig_shape[0]
				node_str.append(NODE_TEMPLATE.format(n_id, base_x + x * node_resolution,
																						base_y + y * node_resolution))
				if all([x > 0, boolean_array[x-1,y]]):
						edge_str.append(EDGE_TEMPLATE.format(n_id-1, n_id))
				if all([y > 0, boolean_array[x,y-1]]):
						edge_str.append(EDGE_TEMPLATE.format(n_id-orig_shape[0], n_id))
	out_str.append('\n'.join(node_str))
	out_str.append('\t\t</nodes>')
	out_str.append('\t\t<edges>')
	out_str.append('\n'.join(edge_str))
	out_str.append('\t\t</edges>')
	out_str.append('\t</graph>')
	out_str.append('</knot>')
	with open(output_file, "w") as f:
		f.writelines(out_str)

if __name__ == "__main__":
	boolean_array = np.load('smallest_bool_matrix.npy').T
	N = 1
	for i in range(N):
		section = int(boolean_array.shape[1] / N)
		main(boolean_array[:, (i*section):((i+1)*section)], node_resolution=30, output_file="boolean_{}.knot".format(i+1))
