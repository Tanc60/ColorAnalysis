# importing required libraries
import numpy as np  
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from ImageIO import ImageIO

  
# creating random dataset
image = ImageIO.GetImageFromFileCV("E:\\Downloads\\gluonCV\\test\\2L7A0030.JPG")
image = ImageIO.ResizeImgCV(image,(30,20))


fig = plt.figure()
plt.figure(figsize = (10, 4))
ax = fig.add_subplot(projection='3d')
image = image.reshape(-1,3)
for element in image:
    ax.scatter(element[0],element[1],element[2])

  
# creating figure
fig = plt.figure()
ax = Axes3D(fig)
  
  
# setting title and labels
ax.set_xlabel('x-axis')
ax.set_ylabel('y-axis')
ax.set_zlabel('z-axis')
  
# displaying the plot
plt.show()