import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def add_padding(image, target_width, target_height):
    # Get the current dimensions of the image
    height, width = image.shape[:2]

    # Calculate the padding needed for width and height
    pad_width = (target_width - width) // 2
    pad_height = (target_height - height) // 2

    # Add padding to the image
    padded_image = cv.copyMakeBorder(image, pad_height, pad_height, pad_width, pad_width,
                                     cv.BORDER_CONSTANT, value=[0, 0, 0])

    return padded_image
def fix_size(img, width, height):
    h, w = img.shape[:2]
    if w < width and h < height:
        img = add_padding(img, w, h, width, height)
    elif w >= width and h < height:
        new_w = width
        new_h = int(h * new_w / w)
        new_img = cv.resize(img, (new_w, new_h), interpolation=cv.INTER_AREA)
        img = add_padding(new_img, new_w, new_h, width, height)
    elif w < width and h >= height:
        new_h = height
        new_w = int(w * new_h / h)
        new_img = cv.resize(img, (new_w, new_h), interpolation=cv.INTER_AREA)
        img = add_padding(new_img, new_w, new_h, width, height)
    else:
        '''w>=target_w and h>=target_h '''
        ratio = max(w / width, h / height)
        new_w = max(min(width, int(w / ratio)), 1)
        new_h = max(min(height, int(h / ratio)), 1)
        new_img = cv.resize(img, (new_w, new_h), interpolation=cv.INTER_AREA)
        img = add_padding(new_img, new_w, new_h, width, height)
    return img

def preprocess_image(image_path, img_width, img_height):
    # Read the image
    img = cv.imread(image_path)

    # Resize the image using fix size
    img = fix_size(img, img_width, img_height)

    img = np.clip(img, 0, 255)
    img = np.uint8(img)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Normalize the pixel values to the range [0, 1]
    img = img / 255.0

    # Convert to float32
    img = img.astype(np.float32)

    return img