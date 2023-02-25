from Segmentation import Segmentation
from ImageIO import ImageIO
from ColorAnalysis import ColorAnalysis

from ImageAnalysis import ImageAnalysis
import ImageDB
import json
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv

#统计分析图像结果，输出json文件，分析图像包含的颜色种类，和每种颜色出现的频数，每张图片对应一个json文件
def ResultAnalysis(sourceDir,targetDir):
    os.chdir(sourceDir)
    if(os.path.isdir(targetDir) == False):
        os.mkdir(targetDir)
    print(os.getcwd())
    filenames = os.listdir()
    ImagedataList=[]
    for filename in filenames:
        Image = ImageIO.GetImageFromFileCV(filename)
        print("-------------------------" + filename + "-------------------------")
        (unique,counts)=ImageAnalysis.ColorDistribution2(Image)
        imageData = ImageDB.Image(filename,unique,counts)

        #暂时没用上
        ImagedataList.append(imageData)

        #输出json文件
        filenamewithoutextension=filename.split(".")[0] #删去扩展名
        with open(targetDir+"/"+filenamewithoutextension+".json",'w',encoding='utf-8') as f:
            json.dump(imageData.__dict__, f,ensure_ascii=False)  #转换为字典类型才能序列化 使用内置函数__dict__

        #绘制柱状图
        plt.figure(figsize = (12, 8))
        plt.bar(unique,counts,color = unique)
        plt.savefig(targetDir+"/"+filenamewithoutextension+".png")
        plt.close()



#从json文件中读取数据，未完成
def MuitiKmeansAnalysisFromJson(sourcejsonDir,targetDir,K):
    os.chdir(sourcejsonDir)
    if(os.path.isdir(targetDir) == False):
        os.mkdir(targetDir)
    print(os.getcwd())
    filenames = os.listdir()
    #最终合成的list
    finalList=[]
    #筛选文件夹中的json文件
    jsonFileCount=0    
    for filename in filenames:

        if filename.split(".")[1]=="json":
            with open(filename, encoding='utf-8') as a:
                # 读取文件
                result = json.load(a)
                # 获取文件名
                print(result.get('name'))  
                # 获取颜色
                uniqueColors=result.get('uniqueColors')
                # 获取颜色数量
                colorCounts=result.get('colorCounts')
                averageColorCount=AverageColorCount(colorCounts)
                print(averageColorCount)
                #每个json文件合成的list
                targetList=GenerateList(uniqueColors,averageColorCount)

                finalList=finalList + targetList
            jsonFileCount=jsonFileCount+1
    print(str(jsonFileCount)+" Json files in total are processed in target directory")

    finalList=np.float32(np.array(finalList)) 
    
    #kmeans聚类
    print("Start kmeans, K="+str(K))

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret,label,center=cv.kmeans(finalList,K,None,criteria,10,cv.KMEANS_RANDOM_CENTERS)
    print(label)
    print(center)

    center = np.uint8(center)
    res = center[label.flatten()]
    #转换为正常的图片形式
    res2 = res.reshape((-1,600,3))
    #rgb to bgr
    res2 = cv.cvtColor(res2, cv.COLOR_BGR2RGB)

    print("generating result in target directory: "+targetDir)
    ResultAnalysis(res2,targetDir)

def AverageColorCount(colorCounts):
    average=[]
    for color in colorCounts:
        result=int(color*400*600/sum(colorCounts))
        average.append(result)
    return average
def GenerateList(uniqueColors,averageColorCount):
    resultList=[]
    for i in range(len(uniqueColors)):
        rgbColor=ImageAnalysis.hex_to_rgb(uniqueColors[i])
        a=[rgbColor]*averageColorCount[i]
        resultList=resultList+a
    return resultList


#待完善,输入一张或多张图片，输出颜色分析图和json文件，可实现multikmeans的分析图
def ResultAnalysis(sourceImage,targetDir):

    (unique,counts)=ImageAnalysis.ColorDistribution2(sourceImage)

    imageData = ImageDB.Image("resultImg",unique,counts)
    with open(targetDir+"/resultImg.json",'w',encoding='utf-8') as f:
            json.dump(imageData.__dict__, f,ensure_ascii=False)
    #由于黑色为蒙版颜色，绘图时的统计结果去掉黑色数据
    for i in range(len(unique)):
        if unique[i] == '#000000':
            unique=np.delete(unique,i)
            counts=np.delete(counts,i)
            break

    plt.figure(figsize = (12, 8))
    plt.bar(unique,counts,color = unique)
    plt.savefig(targetDir+"/resultImg.png")
    plt.close()
"""
def ResultAnalysis(unique,counts,targetDir):

    hexcolorlist=[]
    for i in range(len(unique)):
        hexcolorlist.append(ImageAnalysis.rgb_to_hex(unique[i]))

    plt.figure(figsize = (12, 8))
    plt.bar(hexcolorlist,counts,color = hexcolorlist)
    plt.savefig(targetDir+"/resultImg.png")
    plt.close()
"""

def MuitiKmeansAnalysis(sourceDir,targetDir,K):
    os.chdir(sourceDir)
    print(os.getcwd())
    filenames = os.listdir()
    Imgs=[]
    for filename in filenames:
        Image = ImageIO.GetImageFromFileCV(filename)
        Image = ImageIO.ResizeImgCV(Image,(300,200))
        Imgs.append(Image)
        print("-------------------------" + filename + "-------------------------")
    print("Calculating Kmeans Result from "+ str(len(Imgs)) + " images-------------------------")
    (resultImageList,resultImages) = ColorAnalysis.MuitiKmeans(Imgs,K)
    #ImageIO.PltImg(bar)
    
    ResultAnalysis(resultImages,targetDir)
    print("JsonFile Exported in the following directory: "+ targetDir)

    for i in range(len(resultImageList)):
        #ImageIO.PltImg(resultImgs[i])
        #ImageIO.PltImg(resultImgs[i][:,:,::-1])
        ImageIO.SaveImage(filenames[i],resultImageList[i],"Kmeans",targetDir)
        #np.save(filenames[i].split(".")[0]+".txt",resultImgs[i])
    print("Result images exported in the following directory: "+ targetDir)

  



def SingleKmeansAnalysis(sourceDir,targetDir,K):
    os.chdir(sourceDir)
    print(os.getcwd())
    filenames = os.listdir()

    for filename in filenames:
        Image = ImageIO.GetImageFromFileCV(filename)
        Image = ImageIO.ResizeImgCV(Image,(300,200))

        print("-------------------------" + filename + "-------------------------")
        (res2,ret,label,center) = ColorAnalysis.KmeansSeg(Image,K)
        ImageIO.SaveImage(filename,res2,"Kmeans",targetDir)

def SegmentationAnalysis(sourceDir,targetDir,labels):
    os.chdir(sourceDir)
    print(os.getcwd())
    filenames = os.listdir()
    MaskedImgs=[]
    for filename in filenames:
        Image = ImageIO.GetImageFromFile(filename)
        Image = ImageIO.ResizeImg(Image)
        predict = Segmentation.Segmentation(Image)

        colorMaskedImg = Segmentation.MakeColorMask(predict,filename.split(".")[0]+"color.png")
        #save PIL.image
        baseName=filename.split(".")[0]
        savePath=os.path.join(targetDir, baseName+"color.png")
        colorMaskedImg.save(savePath)
        #ImageIO.SaveImage(filename,colorMaskedImg,"color",targetDir)

        #ImageIO.PltImg(colorMaskedImg)
        
        monoMaskedImg = Segmentation.MakeMonoMask(Image,predict,labels)
        monoMaskedImg = monoMaskedImg[:,:,::-1]  #bgr to rgb
        ImageIO.SaveImage(filename,monoMaskedImg," mono",targetDir)
        #ImageIO.PltImg(monoMaskedImg)

        MaskedImgs.append(monoMaskedImg)


def ModifiedKmeansAnaylsis(SourceDir, targetDir, K, scale):
    os.chdir(SourceDir)
    print(os.getcwd())
    filenames = os.listdir()
    for filename in filenames:
        ModifiedKmeans(filename, targetDir, K, scale)


#-------------------------------------------------Multi-Iteration Method----------------------------------------------
def ModifiedKmeans(filename, targetDir, KList, scale):
    image = ImageIO.GetImageFromFileCV(filename)
    image = ImageIO.ResizeImgCV(image,(300,200))


    #1st kmeans
    #PltImg(image[:,:,::-1])

    #reshape 
   
    inputImg = image.reshape(-1,3)
   
    for i in KList:


        #kmeans
        (resultImg,_,labels,centers)=ColorAnalysis.KmeansSeg(inputImg,i)
        #resultImg------>inputImg colormap
        '''
        colormap=[]
        temp=[]
        originImg = image.reshape(-1,3)
        for i in range(len(labels)):

            colormap.append((centers[labels[i]],inputImg[i]))
            
        #colormap=np.unique(colormap)
        '''

        #-------------------process the mod_res-----------------------
        mod_res=resultImg.copy()
        #unique
        (mod_res,indices,imgcounts)=np.unique(mod_res,axis=0,return_counts=True,return_index=True)
        #preseve order
        #mod_res=mod_res[np.argsort(indices)]

        #process the imgcounts, reduce the difference by the scale factor

        mod_counts=Smoothlist(imgcounts,scale)
        #repeat imgcounts
        mod_res=np.repeat(mod_res,mod_counts,axis=0)
        difference=image.shape[0]*image.shape[1]-mod_res.shape[0]*mod_res.shape[1]
        if difference > 0:
            mod_res=np.pad(mod_res,((0,difference),(0,0)),"wrap")

        #------------rebuid image--------------

        

        #PltImg(real_res)

        print("------------------"+ str(i) +"------------------------")
        print("------------------"+ filename +"------------------------")

        #reset the input value
        inputImg=mod_res



    #result=result.reshape(1,-1,3)

    """
    plt.figure(figsize = (6, 4))
    a=np.array([10]*result.shape[0])
    plt.bar(result,a,color = result)
    """

    #PltImg(image)

    #plot graph
    (unique,counts)=ImageAnalysis.ColorDistribution2(mod_res.reshape(1,-1,3))

    filenamewithoutextension=filename.split(".")[0] #删去扩展名

    plt.figure(figsize = (12, 8))
    plt.bar(unique,counts,color = unique)
    plt.savefig(targetDir+"/"+filenamewithoutextension+".png")
    plt.close()


def Smoothlist(inputList,scale):
    workingList = inputList.copy()
    avg=np.average(workingList)
    for i in range(len(workingList)):
        workingList[i]=avg+scale*(workingList[i]-avg)
    return workingList






if __name__ =="__main__":
    

    while True:
        source = input("Please input the sourcefolder directory (example:E:\\testfile)")
        if(os.path.isdir(source)):
            break   #若输入的正确，则退出循环
        print('invalid folder path, try again.')


    while True:
        target = input("Please input the targetfolder directory (example:E:\\resultfile)")
        if(os.path.isdir(target)):
            break   #若输入的正确，则退出循环
        print('invalid folder path, try again.')

    #arr = input("Please input label index, using SPACE to separate values:(example:0 1 2)")
    #labels = [int(n) for n in arr.split()]

    #SegmentationAnalysis(source,target,labels)
    
    print("Please input K number (example:15)")
    K=input()


    MuitiKmeansAnalysisFromJson(source,target,int(K))
    #MuitiKmeansAnalysis(source,target,int(K))

    #SingleKmeansAnalysis(source,target,int(K))

    #MuitiKmeansAnalysis("E:\Downloads\BaiduNetdiskDownload\suercuntest","E:\Downloads\BaiduNetdiskDownload\suercunMultiKmeans")

    #ResultAnalysis(source,target)