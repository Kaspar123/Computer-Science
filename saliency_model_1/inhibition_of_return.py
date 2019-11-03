import cv2
import numpy as np
import utils
import matplotlib.pyplot as plt

def find_winner_location(saliency_map: np.ndarray, block_size: int):
    height, width = saliency_map.shape
    x_es = np.arange(0, width, block_size)
    y_es = np.arange(0, height, block_size)

    winner_val = 0
    winner_x, winner_y = 0, 0
    for x in x_es:
        for y in y_es:
            block = saliency_map[y:y+block_size, x:x+block_size]
            max_val = np.max(block)
            if (max_val > winner_val):
                winner_x = x
                winner_y = y
                winner_val = max_val
    
    return winner_val, winner_x, winner_y

def draw_salient_circles(image: np.ndarray, centers, radius: int):
    for i in range(len(centers)):
        p = centers[i]
        color = (255, 0, 0) if i == 0 else (0, 255, 255)
        cv2.circle(image, p, radius, color, 2)
    for i in range(len(centers) - 1):
        p1, p2 = centers[i], centers[i + 1]
        cv2.arrowedLine(image, p1, p2, (0, 0, 255), 1, tipLength=0.05)

def saliency_row(saliency_map_filename: str, image_filename: str, width: int, height: int, block_size: int, n: int):
    # load saliency map
    saliency_map = cv2.imread(saliency_map_filename, cv2.IMREAD_GRAYSCALE)
    sal_img = utils.load_image_into_shape(saliency_map, width, height)

    # load corresponding image
    image = cv2.imread(image_filename, cv2.IMREAD_COLOR)
    image = utils.load_image_into_shape(image, width, height)
    
    # calculating ratios
    height, width = saliency_map.shape
    image_height, image_width, _ = image.shape
    k_x = image_width / width
    k_y = image_height / height

    # find salient centers
    salient_centers = []
    for i in range(n):
        val, x, y = find_winner_location(saliency_map, block_size)
        saliency_map[y:y+block_size, x:x+block_size] = 0
        x_image = int((x + block_size / 2) * k_x)
        y_image = int((y + block_size / 2) * k_y)
        salient_centers.append((x_image, y_image))

    # draw circles at centers
    draw_salient_circles(image, salient_centers, 20)

    return {'saliency_map': sal_img, 'image': image}

if __name__ == '__main__':
    width, height = 480, 360
    block_size, n = 10, 5

    filenames = [
        ['output/saliency_poder.jpg', 'source/poder.jpg'],
        ['output/saliency_minu.jpg', 'source/minu.jpg'],
        ['output/saliency_sign.jpg', 'source/sign.jpg'],
    ]

    keys = ['saliency_map', 'image']

    fig, axes = plt.subplots(3, 2, figsize=(15, 15), gridspec_kw = {'wspace':0, 'hspace':0.05})
    for i in range(len(axes)):
        row = saliency_row(filenames[i][0], filenames[i][1], width, height, block_size, n)
        for j in range(len(axes[i])):
            ax = axes[i][j]
            plt.setp(ax.get_xticklabels(), visible=False)
            plt.setp(ax.get_yticklabels(), visible=False)
            key = keys[j]
            ax.imshow(cv2.cvtColor(row[key], cv2.COLOR_BGR2RGB))

    plt.savefig('result.png')