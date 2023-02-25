import numpy as np
import cv2 

from matplotlib import colors
import matplotlib.pyplot as plt


class ImageAnalysis:
    
    
    # rgb 表达方式转化
    def ColorDistribution2(image):
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            modified_img = image.reshape(image.shape[0]*image.shape[1], 3)
            hexcolorlist=[]
            for i in range(len(modified_img)):
                #去掉黑色
                if (ImageAnalysis.rgb_to_hex(modified_img[i]) != "#000000"):
                    hexcolorlist.append(ImageAnalysis.rgb_to_hex(modified_img[i]))

            unique,counts=np.unique(hexcolorlist,return_counts=True)

            return (unique,counts)
        



    @staticmethod
    def rgb_to_hex(rgb_color):
        hex_color = "#"
        for i in rgb_color:
            num = int(i)
            #hex_color += ("{:02x}".format(i))
            hex_color += str(hex(num))[-2:].replace("x","0").upper()
        return hex_color
    

    @staticmethod
    def hex_to_rgb(hex):
        hex = hex.lstrip('#')
        r= int(hex[0:2],16)
        g= int(hex[2:4],16)
        b= int(hex[4:6],16)
        rgb = [r,g,b]
        return rgb