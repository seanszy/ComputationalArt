""" TODO: Put your header comment here """

import random
from PIL import Image
import math


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    # TODO: implement this
    from random import randint
    count = 0

    #returns x once the maximum depth is reached
    #this occurs when the minimum depth is equal to 0
    if min_depth == 0:
        random_one = randint(0,1)
        #choose x or y randomly based on an integer either 0 or 1
        if random_one == 0:
            return ["x"]
        if random_one == 1:
            return ["y"]
    #choose the random depth to go to. Then set the min and max depth to it, so it will be that for each recursive call
    choose_depth = randint(0,max_depth-min_depth)
    min_depth = min_depth+choose_depth
    max_depth = min_depth

    #list of possible functions. One list for functions with one argument, one for two arguments
    single_variable_list = ["sin", "cos", "raise_power", "sr"]
    double_variable_list = ["avg", "prod"]
    random_two = randint(0,1)
    #randomly chooses to go to either one or two variable function
    if random_two == 0:
        random_three = randint(0, 3)
        #randomly selects one of the functions in the single variable list
        return [single_variable_list[random_three], build_random_function(min_depth-1, max_depth-1)]
    else:
        random_four = randint(,1)
        #randomly selects one of the functions in the two variable list
        return [double_variable_list[random_four], build_random_function(min_depth-1, max_depth-1), build_random_function(min_depth-1, max_depth-1)]

def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    # TODO: implement this
    #this is used to make sense of the input coming from build random function.
    #The if statements figure out which operation it is and then conducts the operation
    if f[0] == 'x':
        return x
    if f[0] == 'y':
        return y
    if f[0] == 'sin':
        return math.sin(3.14*evaluate_random_function(f[1], x, y))
        #conducts math.sin of the next item in the list at a lower depth. This is
        #what actually computes the values
        #A similair thing occurs for other functions but with id
    if f[0] == 'cos':
        return math.cos(3.14*evaluate_random_function(f[1], x, y))
    if f[0] == 'prod':
        return (evaluate_random_function(f[1], x, y) * evaluate_random_function(f[2], x, y))
    if f[0] == 'raise_power':
        return (evaluate_random_function(f[1], x, y)**2)
    if f[0] == 'avg':
        return ((evaluate_random_function(f[1], x, y) + evaluate_random_function(f[2],x, y))/2)
    if f[0] == 'sr':
        return math.sqrt(abs(evaluate_random_function(f[1],x, y)))



def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
        >>> remap_interval(90, 0, 100, 10, 20)
        19.0
    """
    # TODO: implement this
    #another test was added to make sure that it was mapping correctly. The test I added
    #was easy to compute by hand, so I could make sure that it is right.
    input_width = input_interval_end-input_interval_start
    output_width = output_interval_end-output_interval_start
    #above finds the width of the input and output
    input_length_from_end = val-input_interval_start
    percentage_input = input_length_from_end/input_width
    #uses input width to calculate what percentage of the first interval the value is
    input_position = output_interval_start + output_width*percentage_input
    #maps the value to the same percentage of the output
    return input_position

def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    #remaps from -1 to 1 to 0 to 255 so it can be a color
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    #test function is no longer used
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=500, y_size=500):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    min_d,max_d = 7,9
    #generates 3 functions with the min and max depth as defined above
    red_function = build_random_function(min_d, max_d)
    print("red ", red_function)
    green_function = build_random_function(min_d, max_d)
    print("green ", red_function)
    blue_function = build_random_function(min_d, max_d)
    print("blue ", blue_function)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    #goes through for loops to set the pixel color based on the funtion at each pixel in the range
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    # 0,0)
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    #doctest.run_docstring_examples(build_random_function, globals(), verbose=True)
    doctest.testmod()
    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
