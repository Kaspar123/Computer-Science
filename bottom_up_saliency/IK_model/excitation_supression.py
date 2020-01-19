import cv2
import numpy as np
import utils

if __name__ == '__main__':
    shape = 480, 640
    height, width = shape

    sigma_1 = 0.02 * width
    sigma_2 = 0.25 * width

    ## normalize
    image = cv2.imread('features/orientation/feature_map_o1_1_3.jpg', cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (width, height))
    image = utils.scale_with_max(image, 1.0)

    for i in range(10):
        cv2.imshow('image', image)
        cv2.waitKey(0)
        image = utils.excitation_suppression(image, sigma_1, sigma_2)

    cv2.destroyAllWindows()