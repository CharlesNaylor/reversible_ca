""" Cellular Automaton Generator

For use in deciding the printed carpet layout I'd like.

These are Wolfram's reversible automata, and so each cell depends on the previous 2 rows. E.g., in a 3x3 matrix:
      1 
    0 1 1
      1 

Could be a rule. Rules are specified as a number from 1 to 256, where the binary expansion shows the result in the bottom-most box if the top-most box is 0. Rules are reversed if the top-most box is 1, allowing the whole system to be reversible. Order from chaos!
The middle row is assumed to be:
    0 0 0, 0 0 1, 0 1 0, 0 1 1, 1 0 0, 1 0 1, 1 1 0, 1 1 1
i.e., the binary expansion of range(8).

The dimensions of the hallway are at most 28" by 146". 

Reverse a pattern by providing the correct starting state, and then row_starting_state + 1 for prior_state.
"""

import numpy as np

def __tuple_to_int(p_tuple):
    return int('%s%s%s' % p_tuple, 2)

def bool_to_bin(bool_row):
    return ''.join([str(x) for x in np.where(bool_row,1,0)])

def run_rule(rule_num=220, dimensions=(10000, 100), starting_state=bin(50000L)[2:], prior_state=None,
             wrap_around=True,):
    """Run the cellular automata.

    :param rule_num: the decimal rule to follow. Rules apply to the previous 2 rows, specifically the 3 neighbors in the previous row, and the middle (same column) cell in the penultimate row. Rules are specified as a number from 1 to 256, where the binary expansion shows the result in the bottom-most box if the top-most box is 0. Rules are reversed if the top-most box is 1, allowing the whole system to be reversible. The middle row is specified as the binary expansion of range(8).
    :type rule_num: int
    :param dimensions: the dimensions of the system. Rows by columns
    :type dimensions: tuple of ints
    :param starting_state: the binary representation of the first row of the output. 
    :type starting_state: str
    :param prior_state: the binary representation of the 0th row of the output (if any)
    :type prior_state: str
    :param wrap_around: does the system wrap around (i.e., the cells are on a cylinder, not a flat surface)?
    :type wrap_around: bool
    """
    if not len(dimensions) == 2:
        raise Exception("You need to give 2 dimensions. You gave {0}".format(len(dimensions)))
    if not 0 <= rule_num <= 255:
        raise Exception("Rule_num must be between 0 and 255. You passed {0}".format(rule_num))
    if len(starting_state) < dimensions[1]:
        starting_state = starting_state * (dimensions[1] / len(starting_state))

    ans = np.zeros(dimensions, dtype=bool)
    rule = "{0:08b}".format(rule_num)
 
    for i in range(dimensions[0]):
        if i == 0: #initial row
            ans[i] = [bool(int(t)) for t in starting_state.zfill(dimensions[1])]
        else:
            for x in range(dimensions[1]):
                if i == 1: #If there's no penultimate row, it's considered to be 0s
                    if prior_state is None:
                        flip_rule = False
                    else:
                        flip_rule = bool(int(prior_state[x]))
                else:
                    flip_rule = ans[i-2, x]

                #Wrap Around
                if x == 0: 
                   state = (int(ans[i-1, dimensions[1]-1]), int(ans[i-1,x]), int(ans[i-1, x+1]))
                elif x == (dimensions[1]-1):
                   state = (int(ans[i-1, x-1]), int(ans[i-1, x]), int(ans[i-1, 0]))
                else:
                   state = (int(ans[i-1, x-1]), int(ans[i-1, x]), int(ans[i-1, x+1]))
                ans[i, x] = int(rule[__tuple_to_int(state)]) * 255
                if flip_rule:
                    ans[i, x] = not ans[i, x]
    return ans

def gen_image(bool_matrix, colors=("#BF5264","beige"), figsize=None):
    """Generates an image from a matrix of booleans
                        
    :param bool_matrix: array of booleans
    :type bool_matrix: :py:code:`numpy.ndArray`
    """
    from matplotlib.colors import ColorConverter
    from scipy.misc import toimage
    cc = ColorConverter()
    rgb_colors = [cc.to_rgb(x) for x in colors]
    new_matrix = np.zeros(bool_matrix.shape + (3,))
    for i in range(3):
      new_matrix[:,:,i] = np.where(bool_matrix, rgb_colors[0][i], rgb_colors[1][i])

    img = toimage(new_matrix)
    img.save("ca_smallest.png")

def gen_big_image(bool_matrix, colors=("#BF5264","beige")):
    """Generates an image using PIL instead"""
    from matplotlib.colors import ColorConverter
    from scipy.misc import toimage
    cc = ColorConverter()
    rgb_colors = [cc.to_rgb(x) for x in colors]
    new_matrix = np.zeros(bool_matrix.shape + (3,))
    for i in range(3):
      new_matrix[:,:,i] = np.where(bool_matrix, rgb_colors[0][i], rgb_colors[1][i])

    n_imgs = bool_matrix.shape[0] / 2000
    for i in range(n_imgs):
      img = toimage(new_matrix[i*2000:(i+1)*2000,:,:])
      img.save("ca{0}.png".format(i))

    remainder = bool_matrix.shape[0] % 2000
    if remainder > 0:
      img = toimage(new_matrix[n_imgs*2000:n_imgs*2000+remainder,:,:])
      img.save("ca{0}.png".format(n_imgs))

def original_matrix_pattern():
    """The first pattern I was mailing around."""
    s_s = "0" * 800 + "1" * 799 + "0"*801
    s_s = "1" * 199 + "0" * 400 + "1" * 401 + "1" * 200 + "1"*201 + "0"*400 + "1"*199
    bool_matrix = run_rule(rule_num=122, dimensions=(7201, 2400), starting_state=s_s, wrap_around=False)#, prior_state=p_s)
    s_s = ''.join([str(x) for x in np.where(bool_matrix[7199,:],1,0)])
    p_s = ''.join([str(x) for x in np.where(bool_matrix[7200,:],1,0)])
    bool_matrix = run_rule(rule_num=122, dimensions=(14400, 2400), starting_state=s_s, prior_state=p_s, wrap_around=False)
    np.save("bool_matrix.npy", bool_matrix)
    gen_big_image(bool_matrix)

def smaller_pattern():
    """The carpet people can only do 300 dpi. Celtic knots expand resolution by a 
factor of 20. So 2' x 12' * 300 dpi / 20 = 360 x 2160"""
    s_s = "0" * 50 + "1" * 79 + "0" * 100 + "1" * 81 + "0"*50
    s_s = "0" * 51 + "1" * 51 + "0" * 51 + "1" * 51 + "0" * 51 + "1" * 51 + "0" * 51
    s_s = "0" * 50 + "1" * 100 + "0" * 59 + "1" * 100 + "0"*50
    bool_matrix = run_rule(rule_num=122, dimensions=(1080, 359), starting_state=s_s, wrap_around=False)#, prior_state=p_s)
    s_s = ''.join([str(x) for x in np.where(bool_matrix[1078,:],1,0)])
    p_s = ''.join([str(x) for x in np.where(bool_matrix[1079,:],1,0)])
    bool_matrix = run_rule(rule_num=122, dimensions=(2159, 359), starting_state=s_s, prior_state=p_s, wrap_around=False)
    np.save("small_bool_matrix.npy", bool_matrix)
    gen_image(bool_matrix)
        
def smallest_pattern():
    """Now, the carpet people say they can only do 72 dpi. Celtic knots expand resolution by a 
factor of 20. So 2' x 12' * 72 dpi / 20 = 90 x 522 (minus 1 from each for an edge in the celtic knot)"""
    s_s = "0" * 30 + "1" * 29 + "0" * 30 
    s_s = "0" * 10 + "1" * 11 + "0" * 10 + "1" * 10 + "0"*7 + "1"*10 + "0"*10 + "1"*11 + "0"*10
    bool_matrix = run_rule(rule_num=122, dimensions=(260, 89), starting_state=s_s, wrap_around=False)#, prior_state=p_s)
    s_s = ''.join([str(x) for x in np.where(bool_matrix[258,:],1,0)])
    p_s = ''.join([str(x) for x in np.where(bool_matrix[259,:],1,0)])
    bool_matrix = run_rule(rule_num=122, dimensions=(521, 89), starting_state=s_s, prior_state=p_s, wrap_around=False)
    np.save("smallest_bool_matrix.npy", bool_matrix)
    gen_image(bool_matrix)

if __name__ == "__main__":
    #original_matrix_pattern()
    smaller_pattern()
    #smallest_pattern()
