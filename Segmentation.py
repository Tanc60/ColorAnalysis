#import string
import mxnet as mx
#import mxnet.image
import mxnet.gluon.data.vision.transforms
import gluoncv
import gluoncv.data as gdata
import gluoncv.data.transforms.presets.segmentation
from gluoncv.utils.viz import get_color_pallete
#import os
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
import numpy as np
import cv2



        #image = mx.image.imread(imgname)
        #resize source image
        #image = gdata.transforms.image.imresize(image, 600, 400)
        # plt.imshow(image.asnumpy())
        # plt.show()

class Segmentation:

    def Segmentation(image):
        # using cpu
        ctx = mx.cpu(0)
        # normalize the image using dataset mean
        from gluoncv.data.transforms.presets.segmentation import test_transform

        img = test_transform(image, ctx) #img 和前面的image的shape不同

        # Load the pre-trained model and make prediction
        # get pre-trained model
        model = gluoncv.model_zoo.get_model('deeplab_resnet101_ade', pretrained=True)

        # make prediction using single scale
        output = model.predict(img)
        predict = mx.nd.squeeze(mx.nd.argmax(output, 1)).asnumpy()

        return predict

    
    def MakeMonoMask(originalImg,predict,labels):
        
        monoMask=np.copy(predict)
        for i in range(0,monoMask.shape[0]):
            for j in range(0,monoMask.shape[1]):
                 #需要抠图的颜色代号:labels
                if(monoMask[i,j] in labels):
                    monoMask[i,j]=255
                else:
                    monoMask[i,j]=0
        monoMask=monoMask.astype("uint8")
        maskedImg = cv2.bitwise_and(originalImg.asnumpy(),originalImg.asnumpy(),mask=monoMask)
        return maskedImg#[:,:,::-1]

        #cv2.imwrite(savePath,ColorTransform.ToTransparent(newImage))

    def MakeColorMask(predict,savepath):
        image = get_color_pallete(predict, 'ade20k')
        #image.save(savepath)
        
        return image