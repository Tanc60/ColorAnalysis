# ColorAnalysis
color analysis tool, segmentation, kmeans and statistic analysis


可实现对输入图片的语义分割，输出分割后的抠图结果和彩色蒙版。
 
输入图片（建议横构图，竖构图会强制拉伸成横构图，造成变形）

![image](https://user-images.githubusercontent.com/48271765/219935238-e6455d54-df5b-4604-92b9-ff0e7a8b8e20.png)
  
输出结果

![image](https://user-images.githubusercontent.com/48271765/219935247-4bed22e0-bbbb-4e53-97d1-b560a14e164e.png)
![image](https://user-images.githubusercontent.com/48271765/219935251-52b26f18-4cc4-4a41-b6fe-f6005ef3fc6e.png)





--------------- kmeans method-----------------------

聚类结果受颜色在图像中的占比影响
当K取值较小时，聚类结果容易忽略色彩对比鲜明，但占比较少的颜色


--------------- modified kmeans method ------------------

改进算法采用多层聚类方法
1. 首先采用较大K值（例如k=200）进行初步聚类分析，过滤掉图像中的噪声

2. 删掉聚类结果中的重复值，这样就可以消除颜色占比对聚类结果的影响
（这里根据颜色占比设置颜色重复系数scale，根据系数调节颜色占比和重复值的关系）
0<scale<1 
scale = 0 时，相当于删去所有重复值，每种颜色只出现1次
scale = 1 时，相当于保留所有重复值。
3. 根据scale大小调整颜色占比，对结果进行二次聚类

4. Klist控制聚类的迭代次数和k值
例如klist = 200 100 10，表示依次按200,100,10的顺序进行迭代。


Detail information please see:
https://github.com/Tanc60/ColorAnalysis/blob/main/KmeansIterationMethod/kmeans_iteration.ipynb

