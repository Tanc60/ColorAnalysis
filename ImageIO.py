import mxnet as mx
import gluoncv.data as gdata
import matplotlib.pyplot as plt
import os
import cv2
import numpy as np

class ImageIO:
    
    def GetImageFromFile(filename):

        image = mx.image.imread(filename)
        return image
        
    def ResizeImg(image):
        
        #image = np.asarray(cv2.resize(image,(600,400)))
        image=gdata.transforms.image.imresize(image, 300, 200)
        return image  

    def GetImageFromFileCV(filename):
        image = cv2.imread(filename)
        return image    



    def ResizeImgCV(image,size):
        
        image = np.asarray(cv2.resize(image,size))
        return image  

    def PltImg(image):
        plt.imshow(image)
        plt.show()

    def SaveImage(fileName,image,suffix,save_dir):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        baseName=fileName.split(".")[0]
        savePath=os.path.join(save_dir, baseName+suffix+".png")
        cv2.imwrite(savePath,image)