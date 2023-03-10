from Segmentation import Segmentation
from ImageIO import ImageIO
from ImageAnalysis import ImageAnalysis
import numpy as np
import pandas as pd
import os

class StatisticAnalysis:
    def ColorSourcePair(originImg,segImg):


        #进行语义分割，提取分析结果predict
        predict = Segmentation.Segmentation(originImg)
        predict = predict.flatten().astype(np.uint8)
        

        #将Kmeans结果转换为hexcolor
        segImg=segImg.reshape(-1,3)
        hex_segImg =[]
        for color in segImg:
                inputColor=ImageAnalysis.rgb_to_hex(color.flatten())
                hex_segImg.append(inputColor)


        #整合成一张数据表
        colorDF = pd.DataFrame({"Color":hex_segImg,"label":predict})
        colorDF= colorDF.groupby(["Color","label"])["Color"].count().reset_index(name="Count")

        return colorDF
        #存储为json文件
        
        print(colorDF)

    def ColorSourceAnalysisFromFile(originImgFolder,segImgFolder):

        absfilenames=StatisticAnalysis.get_file_path_by_name(originImgFolder)

        colorDFs = pd.DataFrame()
        for absfilename in absfilenames:
            Image1 = ImageIO.GetImageFromFile(absfilename)
            Image1 = ImageIO.ResizeImg(Image1)

            absfilename2 = segImgFolder+"\\"+os.path.basename(absfilename).split(".")[0]+"_kmeans.png"
            Image2 = ImageIO.GetImageFromFileCV(absfilename2)
            Image2 = ImageIO.ResizeImgCV(Image2,(300,200))
            colorDF=StatisticAnalysis.ColorSourcePair(Image1,Image2)
            colorDFs=pd.concat([colorDFs,colorDF])
        colorDFs=colorDFs.groupby(["Color","label"])["Count"].sum().reset_index(name="Count2")
        colorDFs.to_json(path_or_buf= r"E:\Downloads\BaiduNetdiskDownload\outputColorDF\colorDFs.json")

            
    def get_file_path_by_name(file_dir):
        '''
        获取指定路径下所有文件的绝对路径
        :param file_dir:
        :return:
        '''
        L = []
        for root, dirs, files in os.walk(file_dir):  # 获取所有文件
            for file in files:  # 遍历所有文件名
                #if (os.path.splitext(file)[1] == '.png') or (os.path.splitext(file)[1] == '.jpg'):  
                L.append(os.path.join(root, file))  # 拼接处绝对路径并放入列表
        return L

         
StatisticAnalysis.ColorSourceAnalysisFromFile(r"E:\Downloads\BaiduNetdiskDownload\testfile",r"E:\Downloads\BaiduNetdiskDownload\outputmultikmeans")
"""
#test input
Image = ImageIO.GetImageFromFile(r"E:\Downloads\BaiduNetdiskDownload\testfile\2L7A4756.JPG")
Image = ImageIO.ResizeImg(Image)

segImg = ImageIO.GetImageFromFileCV(r"E:\Downloads\BaiduNetdiskDownload\resultfile\2L7A4756Kmeans.png")
segImg = ImageIO.ResizeImgCV(segImg,(300,200))
#test result
StatisticAnalysis.ColorSourcePair(Image,segImg)
"""
