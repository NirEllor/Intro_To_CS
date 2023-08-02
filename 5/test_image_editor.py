from image_editor import *


def test_seperate_channels():
    assert separate_channels([[[1, 2]]]) == [[[1]], [[2]]]
    assert separate_channels([[[1, 2, 3, 4, 5]]]) == [
        [[1]], [[2]], [[3]], [[4]], [[5]]]
    assert separate_channels(
        [[[1, 2, 3], [1, 2, 3], [1, 2, 3]], [[1, 2, 3], [1, 2, 3], [1, 2, 3]], [
            [1, 2, 3], [1, 2, 3], [1, 2, 3]], [[1, 2, 3], [1, 2, 3], [1, 2, 3]]]) == [[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]], [[2, 2, 2], [2, 2, 2], [2, 2, 2], [2, 2, 2]], [[3, 3, 3], [3, 3, 3], [3, 3, 3], [3, 3, 3]]]


def test_combine_channels():
    assert combine_channels([[[1]], [[2]]]) == [[[1, 2]]]
    assert combine_channels([[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]], [[2, 2, 2], [2, 2, 2], [2, 2, 2], [2, 2, 2]], [[3, 3, 3], [3, 3, 3], [3, 3, 3], [3, 3, 3]]]) == [[[1, 2, 3], [1, 2, 3], [1, 2, 3]], [[1, 2, 3], [1, 2, 3], [1, 2, 3]], [
        [1, 2, 3], [1, 2, 3], [1, 2, 3]], [[1, 2, 3], [1, 2, 3], [1, 2, 3]]]
    assert combine_channels([
        [[1]], [[2]], [[3]], [[4]], [[5]]]) == [[[1, 2, 3, 4, 5]]]


def test_RGB2grayscale():
    assert RGB2grayscale([[[100, 180, 240]]]) == [[163]]
    assert RGB2grayscale([[[200, 0, 14], [15, 6, 50]]]) == [[61, 14]]


def test_blur_kernel():
    assert blur_kernel(3) == [[1/9, 1/9, 1/9],
                              [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]]
    assert blur_kernel(1) == [[1]]


def test_apply_kernel():
    assert apply_kernel([[0, 128, 255]], blur_kernel(3)) == [[14, 128, 241]]
    assert apply_kernel([[10, 20, 30, 40, 50], [8, 16, 24, 32, 40], [6, 12, 18, 24, 30], [4, 8, 12, 16, 20]], blur_kernel(
        5)) == [[12, 20, 26, 34, 44], [11, 17, 22, 27, 34], [10, 16, 20, 24, 29], [7, 11, 16, 18, 21]]


def test_bilinear_interpolation():
    assert bilinear_interpolation([[0, 64], [128, 255]], 0, 0) == 0
    assert bilinear_interpolation([[0, 64], [128, 255]], 1, 1) == 255
    assert bilinear_interpolation([[0, 64], [128, 255]], 0.5, 0.5) == 112
    assert bilinear_interpolation([[0, 64], [128, 255]], 0.5, 1) == 160
    assert bilinear_interpolation([[15, 30, 45, 60, 75], [90, 105, 120, 135, 150],
                                   [165, 180, 195, 210, 225]], 4/5, 8/3) == 115


def test_resize():
    assert resize([[0, 50], [100, 200]], 3, 4) == [
        [0, 17, 33, 50], [50, 75, 100, 125], [100, 133, 167, 200]]


def test_rotate_90():
    assert rotate_90([[1, 2, 3], [4, 5, 6]], 'R') == [[4, 1], [5, 2], [6, 3]]
    assert rotate_90([[1, 2, 3], [4, 5, 6]], 'L') == [[3, 6], [2, 5], [1, 4]]
    assert rotate_90([[[1, 2, 3], [4, 5, 6]], [[0, 5, 9], [255, 200, 7]]], 'L') == [
        [[4, 5, 6], [255, 200, 7]], [[1, 2, 3], [0, 5, 9]]]


def test_get_edges():
    assert get_edges([[200, 50, 200]], 3, 3, 10) == [[255, 0, 255]]


def test_quantize():
    assert quantize([[0, 50, 100], [150, 200, 250]], 8) == [
        [0, 36, 109], [146, 219, 255]]


def test_quantize_colored_image():
    print(quantize_colored_image([[[56, 2, 3], [1, 234, 3], [1, 2, 3]],
                                  [[1, 2, 3], [1, 23, 3], [1, 2, 3]],
                                  [[1, 2, 3], [1, 154, 3], [1, 12, 3]],
                                  [[1, 2, 3], [1, 2, 3], [1, 2, 3]]], 8))


print(quantize([[0, 50, 100], [150, 200, 250]], 8))
[[0, 32, 96], [128, 191, 223]]

print(type(5) == int)
