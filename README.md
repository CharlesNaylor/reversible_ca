# Celtic Knots based on Cellular Automata

In _A New Kind of Science_, Stephen Wolfram demonstrates reversible one-dimensional cellular automata. Using these, you can create a chaotic pattern that resolves into a regular geometric shape, before dissolving again forever more into chaos.

I have a weirdly narrow hallway in my house that needs a custom-sized rug to prevent my toddlers getting splinters. You can use this code to create a long, narrow pattern that looks a bit like a Persian rug in the center, and chaos at either end. This is how my two-year-old learned the words 'order' and 'chaos'.

To make things more interesting, the basic binary pattern can be translated into XML nodes and edges and fed into [Knotter](https://sourceforge.net/projects/knotter/), provided you're willing to take the risk of downloading something from SourceForge.

I can't provide my images as the file sizes are too large. However, in this repo:

 - ca.py implements Wolfram's reversible cellular automata with the regular pattern specified in a numpy matrix.
 - draw_svg.py will repeat an SVG pattern based on the boolean matrix output from ca.py.
 - draw_celtic.py will output an XML file of nodes and edges which is suitable for uploading into Knotter, to turn the binary dots into celtic knots.
