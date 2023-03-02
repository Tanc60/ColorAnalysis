import cv2
import numpy as np

class ColorAnalysis:
    def KmeansSeg(image,K):
    
        data = image.reshape((-1,3))

        #convert black to white
        for i in range(len(data)):
            if data[i].tolist()==[0,0,0]:
                data[i]=[512,512,512]

        # convert to np.float32
        data = np.float32(data)

        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 1.0)
        
        ret,label,center=cv2.kmeans(data,K,None,criteria,10,cv2.KMEANS_PP_CENTERS)
        #print(ret)
        #print(label)
        #print(center)
        
        # Now convert back into uint8, and make original image
        center = np.uint8(center)
        res = center[label.flatten()]
        res2 = res.reshape((image.shape))
        
        return res2,ret,label,center
        


    def MuitiKmeans(imageList,K):
        testImages=[]

        h=int(imageList[0].shape[0])
        w=int(imageList[0].shape[1])

        for image in imageList:
            image_base = image
            #resize image 
            #width= int(image_base.shape[1]/ratio)
            #height = int(image_base.shape[0]/ratio)
            #image_base = cv.resize(image_base,(width,height))
            image_base = image_base.reshape(image_base.shape[0] * image_base.shape[1], 3)
            testImages.append(image_base)
            #np.reshape(testImages)
        testImages=np.asarray(testImages)


        #展示色彩分布表格
        #plt.imshow(testImages)
        #plt.show()
        (resultImages,_,label,center)=ColorAnalysis.KmeansSeg(testImages,K)

        resultImageList = np.array(resultImages).reshape(-1,h,w,3)

        
        #resultImageList:分析后的图像列表 testImages：分析后的所有图片合成的单张图片，用于分析颜色种类和频率
        return (resultImageList,resultImages)


    