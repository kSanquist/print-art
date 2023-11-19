'''
This file handles the creation of the printable image string
 Author : Kyle Sanquist
Version : 1.0
'''

from PIL import Image
from dom_color import dominant_color
from get_params import get_img_params
from colorama import Style
from tqdm import tqdm
import os, time

# Used to clear the screen with a possible delay
def clear(sleep=0):
    time.sleep(sleep)
    os.system('cls') if os.name == 'nt' else os.system('clear')

# Generates the image's string
def generate_img_str(img_path: str, gened_imgs=[]):
    image_params = get_img_params(img_path)
    return get_image_str(img_path, image_params, gened_imgs)

# Prints a single image of choice to the command line
def print_img_str(img_str: str):
    print()
    for row in img_str:
        print(row)
    print(Style.RESET_ALL)

# Prints all images in a given directory to the command line
def print_all_imgs(directory: str):
    clear(1)
    img_strings = []
    generated_imgs = []
    for img in os.listdir(directory):
        if (img[-3:] != "png"):
            continue
        img_path = f"{directory}/{img}"
        img_str = generate_img_str(img_path, generated_imgs)
        img_strings.append(img_str)
        generated_imgs.append(img)

    clear()
    for img_str in img_strings:
        print_img_str(img_str)

# Uses dominant_color() from dom_color.py to read the pixelart image and grabs the
# dominant colors of each square row by row
def get_colors(image_path: str, h_by_block: int, w_by_block: int, block_hw_in_px: int, l_width: int, gened_imgs: list):
    im = Image.open(image_path)
    px_per_block = block_hw_in_px
    line_thickness = l_width
    image_name = image_path.split('/')[-1]

    colors_by_row = []
    left = 0
    upper = 0
    right = px_per_block
    lower = px_per_block
    crop_rect = (left, upper, right, lower)
    
    with tqdm(total=h_by_block, desc="  Rows Generated", unit="iterations") as rows_pbar:  # Progress bar counting rows generated
        for _ in range(h_by_block):
            row_colors = []

            with tqdm(total=w_by_block, desc="Blocks Generated", unit="iterations") as blocks_pbar:  # Progress bar counting blocks in a row generated
                for _ in range(w_by_block):
                    # Crop to single square
                    cropped_im = im.crop(crop_rect)

                    # Get dominant color of square
                    if (block_hw_in_px == 1):
                        clusters = 1
                    elif (block_hw_in_px == 2):
                        clusters = 4
                    else:
                        clusters = 5
                    dom_color = dominant_color(cropped_im, clusters)

                    row_colors.append(dom_color)

                    left += px_per_block + line_thickness
                    right += px_per_block + line_thickness
                    crop_rect = (left, upper, right, lower)

                    blocks_pbar.update(1)
            
            colors_by_row.append(row_colors)
            upper += px_per_block + line_thickness
            lower += px_per_block + line_thickness
            left = 0
            right = px_per_block
            crop_rect = (left, upper, right, lower)

            # Formatting after clearing screen from past print
            clear()
            for img in gened_imgs:
                print(img + " ✓")
            print(f"\nGenerating '{image_name}' ...\n")
            rows_pbar.update(1)
    
    print("\nGeneration Successful!")
    time.sleep(2)
    return colors_by_row


# Used to color the printed blocks
def escape_code(r=0, g=0, b=0) -> str:
    return f'\x1b[38;2;{str((r))};{str(g)};{str(b)}m'


# Uses the dominant colors gathered from get_colors() to create a
# long string representing the image in a printable format
def get_image_str(image_path: str, template_params: tuple, gened_imgs: list):
    h_by_block = template_params[0][0]
    w_by_block = template_params[0][1]
    block_hw_in_px = template_params[1]
    l_width = template_params[2]
    colors = get_colors(image_path, h_by_block, w_by_block,block_hw_in_px, l_width, gened_imgs)
    str_by_row = []

    for row in colors:
        picture = f''
        for color in row:
            picture += f'{escape_code(*color)}██'
        str_by_row.append(picture)

    return str_by_row
