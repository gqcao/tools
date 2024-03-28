#------------------------------------------------------------------------------------
# To rename new pictures as desktop wallpapers
#
# Created by Guanqun Cao
# 28/03/2024
#------------------------------------------------------------------------------------

import numpy
import os 

start_idx = 12
wrk_dir = "pics/"

for idx, file in enumerate(os.listdir(wrk_dir)):
    ext = file.split(".")[1]
    os.rename(wrk_dir + file, str(start_idx + idx).zfill(2) + "." + ext)
