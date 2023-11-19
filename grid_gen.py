'''
This file handles generating the template that the user will use to create their pixel-art
masterpiece and will then later be printed out to the terminal!
 Author : Kyle Sanquist
Version : 1.0
'''

from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import colorchooser
from gen_image import escape_code, clear
from colorama import Style

# Used to check whether all inputs are valid
# in this case, a valid input is a positive, non-zero digit
def check_inputs(*args):
    for arg in args[:-1]:
        if ((not arg.isdigit()) or (not int(arg) > 0)):
            return False
    if (args[-1] == None):
        return False
    return True

# Grabs parameters for building the template
# including width of grid, height of grid, line thickness, width/height of block
def get_user_grid_params(intro=True):
    if intro:
        print("\nWelcome to the grid generator. This program is your first step to pixel-art printing!")
        print("This program creates a transparent PNG of a grid that you will use to make your pixel-art creation!")
        print("To get started, please provide the following information about your grid:")

    print("\n( 1 ) How wide, in grid squares, do you want the template?")
    w_in_blocks_in = input("      [Positive Whole Number] : ")

    print("\n( 2 ) How tall, in grid squares, do you want the template?")
    h_in_blocks_in = input("      [Positive Whole Number] : ")

    print("\n( 3 ) What color do you want the grid lines to be?")
    root = tk.Tk()
    root.withdraw()
    root.call("wm", "attributes", ".", "-topmost", True)
    rgb, hex = colorchooser.askcolor(title="What Grid Line Color Do You Want?")
    print(f"      [Chosen Color Code] : {hex}")
    print(Style.RESET_ALL, end='')

    print("\nADVANCED SETTINGS")
    print("    By default, grid line thickness is set to 3px and grid square height and width are set to 60px")
    print("    (Note: changing these values will not affect how your art appears when printed).")
    okay = input("    Are these parameters okay? [Y/N] : ").upper()[0]
    if okay == 'N':
        print("\n( 1 ) How thick, in pixels, do you want the gird lines?")
        line_width_in = input("      [Positive Whole Number] : ")

        print("\n( 2 ) How tall and wide do you want each grid square, in pixels?")
        px_per_block_in = input("      [Positive Whole Number] : ")
    else:
        line_width_in = "3"
        px_per_block_in = "60"

    inputs_valid = check_inputs(px_per_block_in, w_in_blocks_in, h_in_blocks_in, line_width_in, rgb)
    if not inputs_valid:
        print("\nInvalid input, please make sure you've entered correct information for each value!")
        input("\nPress ENTER to retry...")
        clear()
        get_user_grid_params(intro=True)

    clear()
    colored_block = f'{escape_code(*rgb)}██'
    print(f"\nGRID SQUARE HEIGHT & WIDTH : {px_per_block_in}")
    print(f"            WIDTH x HEIGHT : {w_in_blocks_in} x {h_in_blocks_in}")
    print(f"                LINE COLOR : {hex} {colored_block} {Style.RESET_ALL}")
    print(f"                LINE WIDTH : {line_width_in}")

    print("\nDo these parameters appear correct?")
    confirm_params = input("[Y/N] : ").upper()[0]

    if confirm_params == 'Y':
        str_params = [px_per_block_in, w_in_blocks_in, h_in_blocks_in, line_width_in]
        int_params =  [int(param) for param in str_params]
        gen_grid(rgb, int_params)
    else:
        clear(1)
        get_user_grid_params(intro=True)


# Handles drawing the grid lines of the template
def draw_grid_lines(image: Image, pen_: ImageDraw, 
                    dimension: str, px_per_block_: int, line_width_: int, rgb_: tuple):
    width_offset = (int(line_width_/2))-1 if (line_width_ % 2 == 0) else (int(line_width_/2))  # This is needed to offset width of line drawn
    pt = px_per_block_+width_offset
    dim_bound = image.width if dimension == 'w' else image.height
    while pt < dim_bound:
        line_xy = [(pt, 0), (pt, image.height)] if dimension == 'w' else [(0, pt), (image.width, pt)]
        pen_.line(xy=line_xy, fill=rgb_, width=line_width_)
        pt += px_per_block_+line_width_


# Generates the entire template image and saves it to the templates directory
def gen_template(h_in_blocks_: int, w_in_blocks_: int, px_per_block_: int, line_width_: int, rgb_: tuple):
    width_in_px = ((px_per_block_ + line_width_) * w_in_blocks_) - line_width_
    height_in_px = ((px_per_block_ + line_width_) * h_in_blocks_) - line_width_
    im = Image.new('RGBA', (width_in_px,  height_in_px), color=(0,0,0,0))
    pen = ImageDraw.Draw(im)

    draw_grid_lines(image=im, pen_=pen, dimension='h', 
                    px_per_block_=px_per_block_, line_width_=line_width_, rgb_=rgb_) # Draw vertical grid lines
    draw_grid_lines(image=im, pen_=pen, dimension='w', 
                    px_per_block_=px_per_block_, line_width_=line_width_, rgb_=rgb_)  # Draw horizontal grid lines
    
    im.save(f'./templates/{px_per_block_}px_{w_in_blocks_}x{h_in_blocks_}_{line_width_}lw.png')


# Calls gen_template(), that's about it
def gen_grid(rgb: tuple, grid_params=list[int]):
    px_per_block, w_in_blocks, h_in_blocks, line_width = grid_params
    print("\nGenerating your grid...")
    gen_template(h_in_blocks_=h_in_blocks, w_in_blocks_=w_in_blocks,
                 px_per_block_=px_per_block, line_width_=line_width, rgb_=rgb)
    
    print("\nGrid generated succesfully!")
    print("\nYour generated grid can be found in the 'templates' folder!")
    print("You can now export the grid to a painting program. Once your masterpiece is done,")
    print("click 'SAVE AS' and save it to the 'images' folder and start printing!")
    print("\n!!! NOTE 1 !!!  In your masterpiece, do NOT use the color you chose for your grid!")
    print("                This will make the color scanner angry!")
    print("\n!!! NOTE 2 !!!  Save your masterpiece as a PNG or it will not be printed!")

    input("\nPress ENTER to return...")