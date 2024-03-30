#------------------------------------------------------------------------------#
# To process desktop wallpapers, and functions include
#   - Rename images with an increaing number
#   - Resize images to fit to the screen
#
# Created by Guanqun Cao
# 28/03/2024
#------------------------------------------------------------------------------#

import numpy
import os 
import subprocess
import cv2

# Environment variables
start_idx       = 21
wrk_dir         = "pics/"
screen_width    = 1920   # target width
screen_height   = 1080   # target height

def rename_imgs():
    for idx, file in enumerate(os.listdir(wrk_dir)):
        ext = file.split(".")[1]
        os.rename(wrk_dir + file, str(start_idx + idx).zfill(2) + "." + ext)

def pad_img(img_name, target_color):
    cmd = "convert " + img_name + " -background " + target_color + " -gravity center -extent " + str(screen_width) + "x" + str(screen_height) + " " + img_name
    subprocess.call(cmd, shell=True)

def resize_imgs():
    for idx, file in enumerate(os.listdir(wrk_dir)):
        curr_image = cv2.imread(wrk_dir + file)
        curr_height, curr_width, _ = curr_image.shape
        if curr_width / curr_height > screen_width / screen_height:   # flatter than the target image, so resize according to the screen width
            perc = screen_width / curr_width
            new_width = screen_width
            new_height = int(curr_height * perc)
            new_image = cv2.resize(curr_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            cv2.imwrite(file, new_image)
        else:   # skinnier than the target image, so resize according to the screen height
            perc = screen_height / curr_height
            new_height = screen_height
            new_width = int(curr_width * perc)
            new_image = cv2.resize(curr_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            cv2.imwrite(file, new_image)
        pad_img(file, "white")

if __name__ == "__main__":
    resize_imgs()

