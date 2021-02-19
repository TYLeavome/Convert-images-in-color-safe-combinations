import os
import cv2
import time
import shutil
import numpy as np
from tqdm import tqdm

# set a timer for running this program. 
time_start=time.time()

# giving an input and an output directory. 
filepath_input = "./Images to convert"
filepath_output = os.path.abspath(os.path.join(os.path.join(filepath_input, os.pardir), "Output"))

# if the output dir has already existed, delete it, or make a new one. 
if os.path.exists(filepath_output): 
    shutil.rmtree(filepath_output) 
    os.mkdir(filepath_output)
else: os.mkdir(filepath_output)

def ColorConvert(im):
    b,g,r = cv2.split(im)
    screen = ((1-(1-b/255)*(1-r/255))*255).astype('uint8') # attention！change nparray dtype to suit cv2. 
    return cv2.merge([screen,g,r])

# convert all tif&jpg images in input dir and save to the output dir. 
for root, dirs, files in os.walk(filepath_input, topdown=False): 
    for name in tqdm(files):
        # if a jpeg is present, alarming this. 
        if os.path.isfile(os.path.splitext(os.path.join(filepath_output, name))[0] + ".jpg"):
            print("A jpeg file already exists for %s" % name)
        else:
            outfile = os.path.splitext(os.path.join(filepath_output, name))[0] + ".jpg"
            if os.path.join(root, name)[-9:] == ".DS_Store": pass #ignore .DS_Store file in macOS. 
            elif os.path.splitext(os.path.join(root, name))[1].lower() == ".tif" or ".jpg":
                try:
                    im = cv2.imread(os.path.join(root, name))
                    cvted = ColorConvert(im)
                    cv2.imwrite(outfile, cvted, [int( cv2.IMWRITE_JPEG_QUALITY), 95])
                except Exception:
                    print("cannot convert")
            else: pass

# print the running time. 
time_end=time.time()
print('time cost',time_end-time_start,'s')