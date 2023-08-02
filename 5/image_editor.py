#################################################################
# FILE : image_editor.py
# WRITER : Nir Ellor Waizner , ellorw.nir , 323816678
# EXERCISE : intro2cs ex5 2022-2023
# DESCRIPTION: A simple program that operates an image processing program with various features
#################################################################
import sys

##############################################################################
#                                   Imports                                  #
##############################################################################
from ex5_helper import *
from math import pow, ceil, floor

##############################################################################
#                                 CONSTANTS                                  #
RED_GRAYSCALE = 0.299
GREEN_GRAYSCALE = 0.587
BLUE_GRAYSCALE = 0.114
RIGHT = "R"
LEFT = "L"
CONVERT_GRAYSCALE = "1"
BLUR = "2"
RESIZE = "3"
ROTATE = "4"
EDGES = "5"
QUANTIZE = "6"
SHOW = "7"
EXIT = "8"
COMMA = ","
ALL_OPTIONS = "12345678"
ABC = "abcdefghijklmnopqrstuvwxyz"
USEFUL_CHARS = "!@#$%^&*()_-+=][}{';:/?.,><~`"
POINT = "."
##############################################################################

##############################################################################
#                                  Functions                                 #
##############################################################################


def separate_channels(image: ColoredImage):  # -> List[SingleChannelImage]:
    lst_separated_images = []
    image_rows = len(image)
    image_columns = len(image[0])
    num_of_colors = len(image[0][0])
    for num in range(num_of_colors):
        lst_img_row = []
        for row in range(image_rows):
            lst_img_column = []
            for column in range(image_columns):
                lst_img_column.append(image[row][column][num])
            lst_img_row.append(lst_img_column)
        lst_separated_images.append(lst_img_row)
    return lst_separated_images


def combine_channels(channels: List[SingleChannelImage]):  # -> ColoredImage:
    united_images_list = []
    num_of_pictures = len(channels)
    num_of_rows = len(channels[0])
    num_of_columns = len(channels[0][0])
    for row in range(num_of_rows):  # 0 to 3
        united_img_rows = []
        for column in range(num_of_columns):  # 0 to 4
            united_image_column = []
            for num in range(num_of_pictures):  # 0 to 3
                united_image_column.append(channels[num][row][column])
            united_img_rows.append(united_image_column)
        united_images_list.append(united_img_rows)

    return united_images_list


def grayscale_mechanism(red, green, blue):
    return round(red * RED_GRAYSCALE + green * GREEN_GRAYSCALE + blue * BLUE_GRAYSCALE)


def RGB2grayscale(colored_image: ColoredImage):  # -> SingleChannelImage:
    """This function converts an RGB image to a grayscale image"""
    grayscale_image = []
    num_of_rows = len(colored_image)
    num_of_columns = len(colored_image[0])
    for row in range(num_of_rows):
        grayscale_rows = []
        for column in range(num_of_columns):
            a1 = colored_image[row][column][0]
            a2 = colored_image[row][column][1]
            a3 = colored_image[row][column][2]
            grayscale_rows.append(grayscale_mechanism(a1, a2, a3))
        grayscale_image.append(grayscale_rows)
    return grayscale_image


def blur_kernel(size: int):  # -> Kernel:
    """This function creates a matrix kernel, given a size"""
    kernel = []
    for i in range(size):
        kernel_row = []
        for j in range(size):
            kernel_row.append(1 / pow(size, 2))
        kernel.append(kernel_row)
    return kernel


def is_edge(x, y, image):
    """This function determines if the coordinate is at the image's edges"""
    if x < 0 or y < 0 or x >= len(image) or y >= len(image[0]):
        return True
    return False


def kernel_multiplication(image, kernel, start_point_row, start_point_column):
    """This function calculates the pixel's value by its neighbors in the image and in the kernel"""
    pixel = 0
    size = len(kernel)
    for i in range(start_point_row, start_point_row + size):  # The rows of the square
        for j in range(start_point_column, start_point_column + size):  # The columns of the square
            if is_edge(i, j, image):
                pixel += (image[start_point_row + len(kernel) // 2][start_point_column + len(kernel) // 2]) * \
                         kernel[0][0]
            else:
                pixel += (image[i][j] * kernel[0][0])
    if pixel < 0:
        pixel = 0
    elif pixel > 255:
        pixel = 255
    return round(pixel)


def apply_kernel(image: SingleChannelImage, kernel: Kernel):  # -> SingleChannelImage:
    """This function applies the kernel_multiplication function to each pixel in the image"""
    kernel_image = []
    num_of_rows = len(image)
    num_of_columns = len(image[0])
    for row in range(num_of_rows):
        kernel_row = []
        for column in range(num_of_columns):
            start_kernel_row = row - len(kernel) // 2  # The y coordinate of the upper left point of the square
            start_kernel_column = column - len(kernel) // 2  # The x coordinate of the upper left point of the square
            kernel_row.append(kernel_multiplication(image, kernel, start_kernel_row, start_kernel_column))
        kernel_image.append(kernel_row)
    return kernel_image


def bilinear_interpolation(image: SingleChannelImage, y: float, x: float):
    """This function operates the bilinear interpolating algorithm"""
    """ image - the source image, y - y in source image, x - x in source image"""
    """ Step 1: Getting the values of all vertices of the rectangle in which the point in the source image is located"""
    a_coordinate = (floor(y), floor(x))
    b_coordinate = (ceil(y), floor(x))
    c_coordinate = (floor(y), ceil(x))
    d_coordinate = (ceil(y), ceil(x))
    a = image[a_coordinate[0]][a_coordinate[1]]
    b = image[b_coordinate[0]][b_coordinate[1]]
    c = image[c_coordinate[0]][c_coordinate[1]]
    d = image[d_coordinate[0]][d_coordinate[1]]
    """ Step 2: Calculate (y, x) in modulo 1 form"""
    y_modulo = y % 1
    x_modulo = x % 1
    """ Step 3: Determine the value of (y, x) in the destined image based on a formula"""
    a_formula = a * (1 - x_modulo) * (1 - y_modulo)
    b_formula = b * y_modulo * (1 - x_modulo)
    c_formula = c * x_modulo * (1 - y_modulo)
    d_formula = d * x_modulo * y_modulo
    value = a_formula + b_formula + c_formula + d_formula
    return round(value)


def resize(image: SingleChannelImage, new_height: int, new_width: int):  # SingleChannelImage:
    """This function resizes the image to a desired size"""
    """ Each point in the edges of the destined image will hav the same value of the relevant edges of the source
    image """
    """ Other points in the destined image will be located in the source image, and then we will use the
     bilinear_interpolation function to determine its value"""
    new_image = []
    old_height = len(image)
    old_width = len(image[0])
    for i in range(new_height):  # Destined image rows
        new_image_rows = []
        for j in range(new_width):  # Destined image columns
            if i == 0 and j == 0:
                value = image[i][j]
            elif i == 0 and j == new_width - 1:
                value = image[i][old_width - 1]
            elif i == new_height - 1 and j == 0:
                value = image[old_height - 1][0]
            elif i == new_width - 1 and j == new_height - 1:
                value = image[old_height - 1][old_width - 1]
            else:
                source_i = i / (new_height - 1) * (old_height - 1)
                source_j = j / (new_width - 1) * (old_width - 1)
                # print(source_i)
                # print(source_j)
                value = bilinear_interpolation(image, source_i, source_j)
            new_image_rows.append(value)
        new_image.append(new_image_rows)
    return new_image


def transpose(image):
    """This function creates the transposed image"""
    transposed_image = []
    num_of_rows = len(image)
    num_of_columns = len(image[0])
    for column in range(num_of_columns):
        transposed_columns_image = []
        for row in range(num_of_rows):
            transposed_columns_image.append(image[row][column])
        transposed_image.append(transposed_columns_image)
    return transposed_image


def rotate_90(image: Image, direction: str) -> Image:
    """This function rotates the image by 90 degrees, given a direction"""
    transposed_image = transpose(image)
    if direction == RIGHT:
        transposed_copy = transposed_image.copy()
        rotated = []
        for row in transposed_copy:
            rotated.append(row[::-1])
    else:
        rotated = transposed_image[::-1]
    return rotated


def get_edges(image: SingleChannelImage, blur_size: int, block_size: int, c: float) -> SingleChannelImage:
    """This function created an edges image from a given one, having three parameters:
     Image: The given image by the user
     Blur size: The size of the blurring kernel
     Block size: The size of the average calculating kernel
     Each pixel has a threshold value, calculated by a formula"""
    new_edged_image = []
    kernel = blur_kernel(blur_size)
    blurred_image = apply_kernel(image, kernel)
    r = block_size // 2  # Important for the threshold values
    for i in range(len(image)):
        new_edged_rows = []
        for j in range(len(image[0])):
            avg_kernel = blur_kernel(block_size)
            # todo - If failed during tests - replace i - r with start_kernel_row and i - j with start_kernel_column and
            #  completely remove r from the function
            threshold = ((kernel_multiplication(blurred_image, avg_kernel, i - r, j - r) * 9) -
                         blurred_image[i][j]) / 8 - c
            # todo - might raise an error if the instructions were not understandable
            if threshold > blurred_image[i][j]:
                new_edged_rows.append(0)
            else:
                new_edged_rows.append(255)
        new_edged_image.append(new_edged_rows)
    return new_edged_image


def quantize(image: SingleChannelImage, N: int):  # -> SingleChannelImage:
    """This function creates a posterization of a grayscale image"""
    quantize_image = []
    num_of_rows = len(image)
    num_of_columns = len(image[0])
    for row in range(num_of_rows):
        quantize_rows = []
        for column in range(num_of_columns):
            # print(N)
            formula_part_one = floor(image[row][column] * (N / 256))
            formula_part_two = round(formula_part_one * 255 / (N - 1))
            quantize_rows.append(formula_part_two)
        quantize_image.append(quantize_rows)
    return quantize_image


def quantize_colored_image(image: ColoredImage, N: int):  # -> ColoredImage:
    """This function creates a posterization of an RGB image"""
    new_quantize_colored_image = []
    separated_colored_image = separate_channels(image)
    for img in separated_colored_image:
        new_quantize_colored_image.append(quantize(img, N))
    combined_quantize_colored_image = combine_channels(new_quantize_colored_image)
    return combined_quantize_colored_image


def get_input_features():
    """This function represents the program"""
    welcome = input("Choose a single number of the following features below:\n "
                    "1 - ""convert to grayscale\n 2 - blur\n 3 - resize\n 4 - rotate by 90 degrees\n 5 - create edged "
                    "image\n 6 - ""quantize\n 7 - show image\n 8 - exit\n")
    return welcome


def invalid_input_features():
    """This function asks for a number after an invalid one was entered"""
    invalid = input("Invalid_input. choose a single number of the following features below:\n "
                    "1 - ""convert to grayscale\n 2 - blur\n 3 - resize\n 4 - rotate by 90 degrees\n 5 - create edged "
                    "image\n 6 - ""quantize\n 7 - show image\n 8 - exit\n")
    return invalid


def valid_input_features(welcome):
    """This function checks if the input to thr option's menu is valid"""
    if len(welcome) != 1:
        return False
    if not welcome.isdigit():
        return False
    if welcome not in ALL_OPTIONS:
        return False
    return True


def nothing_changed():
    """If the image is already in grayscale"""
    return "Looks like it's already in GrayScale!"


def grayscale_feature(rgb_image):
    """This function applies the grayscale_feature"""
    if isinstance(rgb_image[0][0], int):
        print(nothing_changed())
        return rgb_image
    else:
        new_grayscale_image = RGB2grayscale(rgb_image)
        return new_grayscale_image


def invalid_detail():
    """General invalid input"""
    return "Invalid input"


def odd_number(string):
    """Whether a number is odd or not"""
    if int(string) % 2 == 0:
        return True
    return False


def check_number_input(string):
    """This functions determines if the number represented by the string is whole, positive"""
    if not string.isdigit():
        return False
    if int(string) < 0 or int(string) % 1 != 0:
        return False
    return True


def blur_feature(image):
    """This function applies the blur_feature"""
    kernel_size = input("Please Enter the size of the kernel for the blur: ")
    if check_number_input(kernel_size) is False or odd_number(kernel_size):
        return False
    new_blurred_rgb_image = []
    if isinstance(image[0][0], int):
        new_blurred_rgb_image = apply_kernel(image, blur_kernel(int(kernel_size)))
        return new_blurred_rgb_image
    separated_image = separate_channels(image)
    for img in separated_image:
        new_blurred_rgb_image.append(apply_kernel(img, blur_kernel(int(kernel_size))))
    new_blurred_rgb_image = combine_channels(new_blurred_rgb_image)
    return new_blurred_rgb_image


def resize_valid_input(string):
    """"This function checks the resize input"""
    if COMMA not in string:
        return False
    if len(string) < 3:
        return False
    for char in string:
        if not char.isdigit() and string.index(char) != string.index(COMMA):
            return False
        if char != COMMA and int(char) <= 1 and (len(string[:string.index(COMMA)]) == 1 or
                                                 len(string[string.index(COMMA) + 1:]) == 1):
            return False
    return True


def resize_feature(image):
    """This function applies the resize_feature"""
    user_input_resize = input("Please enter the expected height and width, separated by a comma: ")
    if not resize_valid_input(user_input_resize):
        return False
    parameters = user_input_resize.split(COMMA)
    height = int(parameters[0])
    width = int(parameters[1])
    new_resized_image = []
    if isinstance(image[0][0], int):
        new_resized_image = resize(image, height, width)
        return new_resized_image
    separated_image = separate_channels(image)
    for img in separated_image:
        new_resized_image.append(resize(img, height, width))
    new_resized_combined = combine_channels(new_resized_image)
    return new_resized_combined


def rotate_valid_input(string):
    """This function checks if the rotate input is valid"""
    if string != RIGHT and string != LEFT:
        return False
    return True


def rotate_feature(image):
    """This function applies the rotate_feature"""
    user_input_rotate = input("Please enter the side in which you want to rotate the image - left (L) or right (R): ")
    if not rotate_valid_input(user_input_rotate):
        return False
    new_rotated_image = []
    if isinstance(image[0][0], int):
        new_rotated_image = rotate_90(image, user_input_rotate)
        return new_rotated_image
    separated_image = separate_channels(image)
    for img in separated_image:
        new_rotated_image.append(rotate_90(img, user_input_rotate))
    new_rotated_combined = combine_channels(new_rotated_image)
    return new_rotated_combined


def commas_valid_input(string):
    """"This function checks if only one or zero commas appear in an input"""
    cnt = 0
    for char in string:
        if char == COMMA:
            cnt += 1
    if cnt != 2:
        return False
    return True


def is_point_max_one(string):
    """"This function checks if only one or zero points appear in an input"""
    cnt = 0
    for char in string:
        if char == POINT:
            cnt += 1
    if cnt >= 2:
        return False
    return True


def check_constant_valid_input(c):
    """"This function checks if the C constant, given as an input, is valid"""
    if is_point_max_one(c) is False:
        return False
    for char in c:  # In case at most one dot is in the string
        if char in ABC or char in ABC.upper():
            return False
        if char in USEFUL_CHARS:
            return False
        if not char.isdigit() and c.index(char) != c.index(POINT):
            return False
    if type(float(c) % 1) == float:
        if float(c) % 1 == 0:
            return int(float(c))
        return float(c)
    if float(c) == 0.0 or int(c) <= 0:
        return False
    return int(c)


def sizes_valid_input(string):
    """"This function checks if the sizes are valid"""
    parameters = string.split(COMMA)
    for num in parameters[:2]:
        if check_number_input(num) is False or int(num) < 2:
            return False
    blur_size = parameters[0]
    block_size = parameters[1]
    c = parameters[2]
    # print(parameters)
    valid_c = check_constant_valid_input(c)
    if valid_c is False:
        return False
    return int(blur_size), int(block_size), valid_c


def edges_valid_input(string):
    """This function checks if the edges_feature input is valid"""
    if len(string) < 5:
        return False
    if commas_valid_input(string) is False:
        return False
    valid_sizes_input = sizes_valid_input(string)
    if valid_sizes_input is False:
        return False
    return valid_sizes_input


def edges_feature(image):
    """This function applies the edges_feature"""
    user_edges = input("Please enter the blur size, the block size and a constant C, separated by a comma: ")
    valid_user_edges = edges_valid_input(user_edges)
    if valid_user_edges is False:
        return False
    new_edged_image = []
    if isinstance(image[0][0], int):
        new_edged_image = get_edges(image, valid_user_edges[0], valid_user_edges[1], valid_user_edges[2])
        return new_edged_image
    separated_image = separate_channels(image)
    for img in separated_image:
        new_edged_image.append(get_edges(img, valid_user_edges[0], valid_user_edges[1], valid_user_edges[2]))
    new_rotated_combined = combine_channels(new_edged_image)
    return new_rotated_combined


def quantize_valid_input(string):
    """This function checks the quantized input"""
    valid_user_quantize = check_number_input(string)
    if valid_user_quantize is False:
        return False
    if int(string) < 2:
        return False
    return int(string)


def quantize_feature(image):
    """This function applies the quantize_feature"""
    user_quantize = input("Please enter the number of desired shades for a quantized image: ")
    valid_user_quantize = quantize_valid_input(user_quantize)
    if valid_user_quantize is False:
        return False
    new_quantize_image = []
    if isinstance(image[0][0], int):
        new_quantize_image = quantize(image, valid_user_quantize)
        return new_quantize_image
    separated_image = separate_channels(image)
    for img in separated_image:
        new_quantize_image.append(quantize(img, valid_user_quantize))
    new_quantize_combined = combine_channels(new_quantize_image)
    return new_quantize_combined


if __name__ == '__main__':
    exit_program = False
    argv = sys.argv
    if len(argv) != 2:
        print(invalid_detail())
        sys.exit()
    else:
        image_path = argv[1]
        image_loading = load_image(image_path)
        while exit_program is False:
            user_input = get_input_features()
            while not valid_input_features(user_input):
                try_again = invalid_input_features()
                user_input = try_again

            if user_input == CONVERT_GRAYSCALE:
                image_loading = (grayscale_feature(image_loading))

            elif user_input == BLUR:
                tmp = blur_feature(image_loading)
                if tmp is False:
                    print(invalid_detail())
                    continue
                image_loading = tmp

            elif user_input == RESIZE:
                tmp = resize_feature(image_loading)
                if tmp is False:
                    print(invalid_detail())
                    continue
                image_loading = tmp

            elif user_input == ROTATE:
                tmp = rotate_feature(image_loading)
                if tmp is False:
                    print(invalid_detail())
                    continue
                image_loading = tmp

            elif user_input == EDGES:
                tmp = edges_feature(image_loading)
                if tmp is False:
                    print(invalid_detail())
                    continue
                image_loading = tmp

            elif user_input == QUANTIZE:
                tmp = quantize_feature(image_loading)
                if tmp is False:
                    print(invalid_detail())
                    continue
                image_loading = tmp

            elif user_input == SHOW:
                show_image(image_loading)

            elif user_input == EXIT:
                exit_input = input("Please enter a path in order to save the image: ")
                save_image(image_loading, exit_input)
                exit_program = True
