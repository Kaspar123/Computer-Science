import cv2
import numpy as np
import utils

def test_pyramid_image(img: np.ndarray, out_file: str, n: int):
    pyramid = utils.vizualize_gaussian_pyramid(img, n)
    pyramid = cv2.normalize(pyramid,None,0,255,cv2.NORM_MINMAX).astype('uint8')
    cv2.imwrite(out_file, pyramid)

def test_image_interpolation(img: np.ndarray, out_file: str):
    height, width = shape
    d = utils.pyramid_dictionary(img, 8)
    img = utils.interpolate_img(d[5], width, height)
    cv2.imwrite(out_file, img)

def test_across_scale_difference(img: np.ndarray, out_file: str, finer_scale: int, coarse_scale: int):
    pyramid = utils.pyramid_dictionary(img, 8)
    difference = utils.across_scale_difference(pyramid, finer_scale, coarse_scale)
    difference = utils.scale(difference)

    cv2.imwrite(out_file, difference)

def test_surround_differences_dictionary_1(img: np.ndarray, out_file: str):
    pyramid = utils.pyramid_dictionary(img, 8)
    c = [1, 2, 3]
    d = [2, 3]

    result = utils.center_surround_differences_dictionary(pyramid, c, d)
    for key in result:
        c, d = key
        out = cv2.normalize(result[key],None,0,255,cv2.NORM_MINMAX).astype('uint8')
        cv2.imwrite('{}_{}_{}.jpg'.format(out_file, c, d), out)

def test_surround_differences_dictionary_2(img_1: np.ndarray, img_2: np.ndarray, out_file: str):
    pyramid_1 = utils.pyramid_dictionary(img_1, 8)
    pyramid_2 = utils.pyramid_dictionary(img_2, 8)
    c = [1, 2, 3]
    d = [2, 3]

    result = utils.center_surround_differences_dictionary_2(pyramid_1, pyramid_2, c, d)
    for key in result:
        c, d = key
        out = cv2.normalize(result[key],None,0,255,cv2.NORM_MINMAX).astype('uint8')
        cv2.imwrite('{}_{}_{}.jpg'.format(out_file, c, d), out)

def test_across_scale_addition_I(intensity_img: np.ndarray, out_file: str):
    pyramid = utils.pyramid_dictionary(intensity_img, 8)
    c = [1, 2, 3]
    d = [2, 3]

    height, width = pyramid[3].shape
    dictionary = utils.center_surround_differences_dictionary(pyramid, c, d)

    result = utils.across_scale_addition(dictionary, width, height)
    image = cv2.normalize(result,None,0,255,cv2.NORM_MINMAX).astype('uint8')
    cv2.imwrite(out_file, image)
    return result

def test_across_scale_addition_C(img_r: np.ndarray, img_g: np.ndarray, img_b: np.ndarray, img_y: np.ndarray, out_file: str):
    pyramid_r = utils.pyramid_dictionary(img_r, 8)
    pyramid_g = utils.pyramid_dictionary(img_g, 8)
    pyramid_b = utils.pyramid_dictionary(img_b, 8)
    pyramid_y = utils.pyramid_dictionary(img_y, 8)

    height, width = pyramid_r[3].shape
    c = [1, 2, 3]
    d = [2, 3]

    dictionary_rg = utils.center_surround_differences_dictionary_2(pyramid_r, pyramid_g, c, d)
    dictionary_by = utils.center_surround_differences_dictionary_2(pyramid_b, pyramid_y, c, d)

    dictionary_rg = dict(((c, d, 'rg'), value) for ((c, d), value) in dictionary_rg.items())
    dictionary_by = dict(((c, d, 'by'), value) for ((c, d), value) in dictionary_by.items())
    dictionary_rg.update(dictionary_by)
    
    result = utils.across_scale_addition(dictionary_rg, width, height)
    image = cv2.normalize(result,None,0,255,cv2.NORM_MINMAX).astype('uint8')
    cv2.imwrite(out_file, image)
    return result



def test_across_scale_addition_O(img_o1: np.ndarray, img_o2: np.ndarray, img_o3: np.ndarray, img_o4: np.ndarray, out_file: str):
    pyramid_o1 = utils.pyramid_dictionary(img_o1, 8)
    pyramid_o2 = utils.pyramid_dictionary(img_o2, 8)
    pyramid_o3 = utils.pyramid_dictionary(img_o3, 8)
    pyramid_o4 = utils.pyramid_dictionary(img_o4, 8)

    height, width = pyramid_o1[3].shape
    c = [1, 2, 3]
    d = [2, 3]
    
    dictionary_o1 = utils.center_surround_differences_dictionary(pyramid_o1, c, d)
    dictionary_o2 = utils.center_surround_differences_dictionary(pyramid_o2, c, d)
    dictionary_o3 = utils.center_surround_differences_dictionary(pyramid_o3, c, d)
    dictionary_o4 = utils.center_surround_differences_dictionary(pyramid_o4, c, d)

    dictionary_o1 = dict(((c, d, 'o1'), value) for ((c, d), value) in dictionary_o1.items())
    dictionary_o2 = dict(((c, d, 'o2'), value) for ((c, d), value) in dictionary_o2.items())
    dictionary_o3 = dict(((c, d, 'o3'), value) for ((c, d), value) in dictionary_o3.items())
    dictionary_o4 = dict(((c, d, 'o4'), value) for ((c, d), value) in dictionary_o4.items())

    dictionary_o1.update(dictionary_o2)
    dictionary_o1.update(dictionary_o3)
    dictionary_o1.update(dictionary_o4)
    
    result = utils.across_scale_addition(dictionary_o1, width, height)
    image = cv2.normalize(result,None,0,255,cv2.NORM_MINMAX).astype('uint8')
    cv2.imwrite(out_file, image)
    return result

def test_saliency_map(intensity: np.ndarray, color: np.ndarray, orientation: np.ndarray, out_file: str):
    # scale to [0..1]
    intensity = utils.scale_with_max(intensity, 1.0)
    color = utils.scale_with_max(color, 1.0)
    orientation = utils.scale_with_max(orientation, 1.0)   

    # apply DoG
    intensity = utils.normalization_operator_new(intensity)
    color = utils.normalization_operator_new(color)
    orientation = utils.normalization_operator_new(orientation)
    result = (intensity + color + orientation) / 3
    
    result = cv2.normalize(result,None,0,255,cv2.NORM_MINMAX).astype('uint8')
    cv2.imwrite(out_file, result)

if __name__ == '__main__':
    filename = 'sign'
    shape = 480, 640
    height, width = shape

    # Intensity
    I = cv2.imread('source/{}.jpg'.format(filename), cv2.IMREAD_GRAYSCALE)
    I = utils.load_image_into_shape(I, width, height)

    I = I / 255.0

    # Color
    color_image = cv2.imread('source/{}.jpg'.format(filename), cv2.IMREAD_COLOR)
    color_image = utils.load_image_into_shape(color_image, width, height)
    R, G, B, Y = utils.extract_RGBY_from_image(color_image)

    R = R / 255.0
    G = G / 255.0
    B = B / 255.0
    Y = Y / 255.0

    # Orientation
    O1, O2, O3, O4 = utils.extract_orientations_from_image(I)

    O1 = utils.scale_with_max(O1, 1.0)
    O2 = utils.scale_with_max(O2, 1.0)
    O3 = utils.scale_with_max(O3, 1.0)
    O4 = utils.scale_with_max(O4, 1.0)

    # Generating pyramids
    test_pyramid_image(I, 'pyramids/pyramid_i.jpg', 8)
    test_pyramid_image(R, 'pyramids/pyramid_r.jpg', 8)
    test_pyramid_image(G, 'pyramids/pyramid_g.jpg', 8)
    test_pyramid_image(B, 'pyramids/pyramid_b.jpg', 8)
    test_pyramid_image(Y, 'pyramids/pyramid_y.jpg', 8)
    test_pyramid_image(O1,'pyramids/pyramid_o_1.jpg', 8)
    test_pyramid_image(O2,'pyramids/pyramid_o_2.jpg', 8)
    test_pyramid_image(O3,'pyramids/pyramid_o_3.jpg', 8)
    test_pyramid_image(O4,'pyramids/pyramid_o_4.jpg', 8)

    # Generating feature maps (6 + 12 + 24)
    test_surround_differences_dictionary_1(I, 'features/intensity/feature_map_i')       # 6 maps
    test_surround_differences_dictionary_2(R, G, 'features/color/feature_map_rg')       # 6 maps
    test_surround_differences_dictionary_2(B, Y, 'features/color/feature_map_by')       # 6 maps
    test_surround_differences_dictionary_1(O1, 'features/orientation/feature_map_o1')   # 6 maps
    test_surround_differences_dictionary_1(O2, 'features/orientation/feature_map_o2')   # 6 maps
    test_surround_differences_dictionary_1(O3, 'features/orientation/feature_map_o3')   # 6 maps
    test_surround_differences_dictionary_1(O4, 'features/orientation/feature_map_o4')   # 6 maps

    # Generating conspicuity maps (3 maps -> I, O, C)
    I_ = test_across_scale_addition_I(I, 'conspicuity_maps/intensity.jpg')
    C_ = test_across_scale_addition_C(R, G, B, Y, 'conspicuity_maps/color.jpg')
    O_ = test_across_scale_addition_O(O1, O2, O3, O4, 'conspicuity_maps/orientation.jpg')

    # Generating saliency map
    test_saliency_map(I_, C_, O_, 'output/saliency_{}.jpg'.format(filename))



