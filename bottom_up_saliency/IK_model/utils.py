import cv2
import math
import numpy as np
from typing import Sequence, Dict, Tuple

def scale(image: np.ndarray) -> np.ndarray :
    return scale_with_max(image, 255.0)

def scale_with_max(image: np.ndarray, max_val: float) -> np.ndarray :
    min_ = image.min()
    max_ = image.max()
    K = max_val / (max_ - min_)
    return K * (image - min_)

def load_image_into_shape(img: np.ndarray, width: int, height: int) -> np.ndarray :
    return cv2.resize(img, (width, height))

def extract_RGBY_from_image(color_image: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray] :
    b, g, r = color_image[:, :, 0], color_image[:, :, 1], color_image[:, :, 2]

    R = r - (g + b) / 2
    G = g - (r + b) / 2
    B = b - (r + g) / 2
    Y = (r + g) / 2 - np.abs(r - g) / 2 - b

    R[R < 0] = 0
    G[G < 0] = 0
    B[B < 0] = 0
    Y[Y < 0] = 0

    return R, G, B, Y

def extract_orientations_from_image(img: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray] :
    sobel_x = cv2.Sobel(img, -1, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(img, -1, 0, 1, ksize=3)

    # [0, 45, 90, 135]
    th0 = sobel_x * np.cos(np.pi * 0.00) + sobel_y * np.sin(np.pi * 0.00)
    th1 = sobel_x * np.cos(np.pi * 0.25) + sobel_y * np.sin(np.pi * 0.25)
    th2 = sobel_x * np.cos(np.pi * 0.50) + sobel_y * np.sin(np.pi * 0.50)
    th3 = sobel_x * np.cos(np.pi * 0.75) + sobel_y * np.sin(np.pi * 0.75)

    return np.abs(th0), np.abs(th1), np.abs(th2), np.abs(th3)

def pyramid_dictionary(img: np.ndarray, n:int) -> Dict[int, np.ndarray] :
    d = {}
    for i in range(n):
        d[i] = img if i == 0 else cv2.pyrDown(d[i-1])
    return d

def vizualize_gaussian_pyramid(img: np.ndarray, n: int) -> np.ndarray :
    height, width = img.shape
    pyramid = np.zeros((math.ceil(height * 1.5), width), dtype=np.float32)

    d = pyramid_dictionary(img, n)

    w, h = 0, 0
    for i in range(n):
        img = d[i]
        h1, w1 = img.shape
        print("level: {}, shape: {}".format(i, img.shape))
        pyramid[h:h+h1, w:w+w1] = img
        w += w1
        if (i == 0):
            w, h = 0, h1
    return pyramid

def interpolate_img(img: np.ndarray, width: int, height: int) -> np.ndarray :
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_LINEAR)

# interpolation to the finer scale and point-by-point subtraction
def across_scale_difference(pyramid: Dict[int, np.ndarray], finer_scale: int, coarse_scale: int) -> np.ndarray :
    height, width = pyramid[finer_scale].shape
    interpolated_img = interpolate_img(pyramid[coarse_scale], width, height)
    return np.abs(interpolated_img - pyramid[finer_scale])

# all feature maps are interpolated to (width, height) and point-by-point addition is done
def across_scale_addition(pyramid: Dict[Tuple[int, int], np.ndarray], width: int, height: int) -> np.ndarray :
    result = np.zeros((height, width), dtype=np.float32)
    for key in pyramid:
        interpolated_image = interpolate_img(pyramid[key], width, height)
        interpolated_image = scale_with_max(interpolated_image, 1.0)
        result += normalization_operator_new(interpolated_image)
    return result

# The more unique the global maximum is, the more it will be
def normalization_operator_old(img: np.ndarray) -> np.ndarray :
    M = np.max(img)
    m = np.mean(img)
    K = (M - m)**2
    return K * img

# DoG is used for excitation of salient regions and suppressing non-salient ones
def excitation_suppression(M: np.ndarray, sigma_1: float, sigma_2: float) -> np.ndarray :
    c_ex = 0.5
    c_inh = 1.5
    g1 = cv2.GaussianBlur(M, (0, 0), sigmaX=sigma_1)
    g2 = cv2.GaussianBlur(M, (0, 0), sigmaX=sigma_2)
    DoG = c_ex**2 * g1 - c_inh**2 * g2
    M = M + DoG
    M[M < 0] = 0
    return M

# subtract result of DoG 10 times from img
def normalization_operator_new(img: np.ndarray) -> np.ndarray :
    M = img
    _, width = img.shape
    sigma_1 = 0.02 * width
    sigma_2 = 0.25 * width
    num_of_iterations = 10

    for _ in range(num_of_iterations):
        M = excitation_suppression(M, sigma_1, sigma_2)

    return M

# c x d amount of difference maps
def center_surround_differences_dictionary(pyramid: Dict[int, np.ndarray], center_layers: Sequence[int], deltas: Sequence[int]) -> Dict[Tuple[int, int], np.ndarray] :
    result = {}
    for c in center_layers:
        for d in deltas:
            s = c + d
            result[(c, s)] = across_scale_difference(pyramid, c, s)
    return result

# two pyramids involved in center surround difference dictionary 
def center_surround_differences_dictionary_2(pyramid_1: Dict[int, np.ndarray], pyramid_2: Dict[int, np.ndarray], center_layers: Sequence[int], deltas: Sequence[int]) -> Dict[Tuple[int, int], np.ndarray] :
    result = {}
    for c in center_layers:
        height, width = pyramid_1[c].shape
        for d in deltas:
            s = c + d
            finer_image, coarser_image = pyramid_1[c] - pyramid_2[c], pyramid_2[s] - pyramid_1[s]
            interpolated_img = interpolate_img(coarser_image, width, height)
            result[(c, s)] = np.abs(finer_image - interpolated_img)
    return result
            

