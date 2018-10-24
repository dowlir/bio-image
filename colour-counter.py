# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:41:54 2018

@author: Rhiannon
"""

import numpy as np
from PIL import Image
import matplotlib
import glob
import pandas as pd
import re

#create empty list to store results
images_list = []
#iterate over the images
#make sure your folder is called images and is in your main dir
for filepath in glob.iglob("images/*.jpg"):
    img = Image.open(filepath)
    #img in jpg works best just dont use format with transparency 
    arr = np.array(img)
    #print(arr)
    #arr = arr[:,:, :3] this was for RGBA to a len 3 array conversion to rem A
    arr = matplotlib.colors.rgb_to_hsv(arr) #conv to hsv
    
    #initiatlise pixel count
    n = 0 
    #initial pale colour pixels
    p = 0
    #initial dark colour pixels
    d = 0
    
    for row in range(0, len(arr)):
        for col in range(0, len(arr[row])):
            #blue is 114 to 178 hue value
            if arr[row][col][0] <178/255 and arr[row][col][0] > 114/255 and arr[row][col][1] > 25/255:
                #hsv values as percentage of 255
                n = n + 1
                #to find low and high levels of expression
                if arr[row][col][2] <120/255:
                    d = d + 1
                else:
                    p = p + 1
            
    #calculate percentage cover of blue
    size = arr.shape
    total_pixels = size[0] * size[1]
    perc_blue = (n/total_pixels)*100
    perc_pale = (p/n)*100
    perc_dark = (d/n)*100
    file_split = re.split(r"\\", filepath)
    jpg_split = re.split(".jpg", file_split[1])
    name_split = re.split("_", jpg_split[0])
    images_list.append([name_split[0], name_split[1], 
                        perc_blue, perc_pale, perc_dark])
    
print(images_list)
    
images_df = pd.DataFrame(images_list, 
                         columns = ["Genotype", "Treatment","PercentBlue",
                                    "PercentPale","PercentDark"])

print(images_df)
images_df.to_csv("GUS_presence.csv")