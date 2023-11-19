'''
This file handles calculating the parameters of the template that is currently being used
 Author : Kyle Sanquist
Version : 1.0
'''

from PIL import Image
import numpy as np
import math

# Gets height and width per block (blocks are square so height = width)
def get_block_dims(color_values: list) -> int:
    count = 1
    set_value = color_values[0]
    for value in color_values[1:len(color_values)]:
        if (set_value == value).all():
            count += 1
            continue
        break
    return count
        
# (left, upper, right, lower)
# Computes the dimension by blocks and the pixels per block
def get_grid_dim(im: Image, dimension: str) -> int:
    dim = im.width if dimension == 'w' else im.height
    crop_bounds = (0, 0, dim, 1) if dimension == 'w' else (0, 0, 1, dim)
    cropped_im_arr = np.asarray(im.crop(crop_bounds))
    color_channels = cropped_im_arr.shape[2]
    color_values = np.asarray(cropped_im_arr.reshape(1, -1, color_channels))[0]
    
    block_hw_px = get_block_dims(color_values)

    bc_attempt = math.floor(dim/block_hw_px)
    block_count = 0
    line_width = 0
    while (True) :  # Used to find block_count and line_width given grid dimension and block height and width
        lw_attempt = (dim - bc_attempt*block_hw_px) / (bc_attempt - 1)
        dim_attempt = ((block_hw_px + lw_attempt) * bc_attempt) - lw_attempt
        if (lw_attempt.is_integer() and lw_attempt > 0 and dim_attempt == dim):
            block_count = bc_attempt
            line_width = int(lw_attempt)
            break
        else:
            bc_attempt -= 1

    return (block_count, block_hw_px, line_width)

# Returns the dimension of the provided image in blocks
def get_img_params(img_path: str) -> tuple:
    im = Image.open(img_path)
    dim = (get_grid_dim(im, 'h')[0], get_grid_dim(im, 'w')[0]) 
    block_hw_px = get_grid_dim(im, 'w')[1]
    l_width = get_grid_dim(im, 'w')[2]

    return dim, block_hw_px, l_width