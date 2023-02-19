import numpy
class Image(object):

    def __init__(self,name,uniqueColors,colorCounts) :
        self.name = name
        self.uniqueColors = numpy.ndarray.tolist(uniqueColors)
        self.colorCounts = numpy.ndarray.tolist(colorCounts)
        
class ImageDB(object):
    def __init__(self,imageList):
        # self.name = name
        self.images = imageList