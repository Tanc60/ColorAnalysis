from matplotlib.patches import Patch
import numpy as np
import cv2 
import os
from matplotlib import colors
import matplotlib.pyplot as plt
import colour
import colorsys
from GlobalParameters import GlobalParameters as GP
import Helper
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
        
    def rgb_to_hex(rgb_color):
        hex_color = "#"
        for i in rgb_color:
            num = int(i)
            #hex_color += ("{:02x}".format(i))
            hex_color += str(hex(num))[-2:].replace("x","0").upper()
        return hex_color
    
    def hex_to_rgb(hex):
        hex = hex.lstrip('#')
        r= int(hex[0:2],16)
        g= int(hex[2:4],16)
        b= int(hex[4:6],16)
        rgb = [r,g,b]
        return rgb

    def hexrgb2munsell(hex):
        rgb=ImageAnalysis.hex_to_rgb(hex)

        unitrgb=[]
        for element in rgb:
             unitrgb.append(element/255.0)

        XYZ = colour.sRGB_to_XYZ(unitrgb)
        xyY = colour.XYZ_to_xyY(XYZ)
        munsell = colour.xyY_to_munsell_colour(xyY)
        return munsell
    

    def HexColorList2HSV(hexcolorlist):
        HSVList :list[str] = []
        for hexcolor in hexcolorlist:
            rgb = ImageAnalysis.hex_to_rgb(hexcolor)
            (h,s,v) = colorsys.rgb_to_hsv(rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0)
            h
            hsv : str = "H"+str(int(h*180))+"S"+str(int(s*255))+"V"+str(int(v*255))
            HSVList.append(hsv)
        return HSVList
            

        


    
    def Img2Graph(InputFilename,OutputFilename)->None:
        '''
        输入图片，输出颜色分布饼图与柱状图
        '''
        image = cv2.imread(InputFilename)
        #image = cv2.imread(r"E:\Downloads\BaiduNetdiskDownload\resultfile3\2L7A4756 mono.png")

        hexcolorlist,counts=ImageAnalysis.ColorDistribution2(image)
        percentages = counts / counts.sum() * 100

        HSVList = ImageAnalysis.HexColorList2HSV(hexcolorlist)

        #原图
        #fig1 = plt.figure(figsize=(5, 5))
        #plt.savefig()
        
        #plt.close()

        #legend
        legend_elements =[]
        for i in range(len(HSVList)):
            legend_elements.append(Patch(facecolor=hexcolorlist[i],label=HSVList[i]))

        #饼图
        fig2 = plt.figure(figsize=(8, 5))
        color_labels = [f'{perc:.1f} %' for label, perc in zip(HSVList, percentages)]
        pie = plt.pie(counts, labels=color_labels, colors=hexcolorlist)

        plt.legend(handles=legend_elements,bbox_to_anchor=(1.1, 1),loc='upper left')

        plt.savefig(OutputFilename + "_pie.png",bbox_inches='tight',pad_inch=0.5)
        plt.close()

        #柱状图
        fig3 = plt.figure(figsize=(8, 5))
        bars = plt.bar(HSVList, counts,width = GP.BarPlotWidth, color=hexcolorlist)
        plt.bar_label(bars, [f'{perc:.1f} %' for perc in percentages])
        
        plt.xticks(HSVList,
                rotation=GP.xticksRotation,
                position = (0,0), #调整年份的位置，让远离了x轴
                fontsize = GP.fontSize) 
        
        plt.legend(handles=legend_elements,bbox_to_anchor=(1, 1),loc='upper left')

        plt.savefig(OutputFilename + "_bar.png",bbox_inches='tight',pad_inch=0.5)
        plt.close()



    def ImageFiles2Graph(filenames,targetDir):
        for filename in filenames:
            print(filename)
            filenamewithoutextension = os.path.basename(filename).split('.')[0] #删去扩展名
            outPutFilename = targetDir + "\\" + filenamewithoutextension
            ImageAnalysis.Img2Graph(filename,outPutFilename)

    def draw_histogram(sourcefilename,targetfilename):
    
        size=64

        img = cv2.imread(sourcefilename)

        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = img2[:,:,0], img2[:,:,1], img2[:,:,2]
        hist_h = cv2.calcHist([h],[0],None,[size],[0,256])
        hist_s = cv2.calcHist([s],[0],None,[size],[0,256])
        hist_v = cv2.calcHist([v],[0],None,[size],[0,256])
        #Hue
        plt.bar(np.arange(0,size),hist_h.reshape(-1),width=1)
        plt.legend("H")
        plt.savefig(Helper.AddSuffixToFullFilename(targetfilename,"_H"))
        plt.close() 
        #Saturation
        plt.bar(np.arange(0,size),hist_s.reshape(-1),width=1)
        plt.legend("S")
        plt.savefig(Helper.AddSuffixToFullFilename(targetfilename,"_S"))
        plt.close()
        #Vue
        plt.bar(np.arange(0,size),hist_v.reshape(-1),width=1)
        plt.legend("V")
        plt.savefig(Helper.AddSuffixToFullFilename(targetfilename,"_V"))
        plt.close()

        hue=hist_h.reshape(-1)

        # Compute pie slices
        N = size
        theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
        radii = (hue*100/hue.max())
        width = 2 * np.pi / N

        colors = plt.cm.hsv(theta/2/np.pi)
        fig = plt.figure(figsize=(6, 6))    
        ax = plt.subplot(111, projection='polar')
        
        bars = ax.bar(theta, radii, width=width, bottom=50, color=colors)
        plt.title("Hue")
        plt.savefig(Helper.AddSuffixToFullFilename(targetfilename,"_H_Pie"))
        plt.close()