"""
author : Michael

"""
from utils import D;
#TODO impelement lazyness level to control processing
#TODO? write method 'die' to write label to self.label then clear the path 
#TODO write static method to read list of lazyImages and return (labels, feature vectors )
# path , hog_vector [, label
class Image(object):
    """lazy images
    """
    def __init__(self, path,lazyness=50):
        self.path=path;
        self.process();
#        self.label=self.getlabel()

    def load(self):# lazy loading
        """load images when needed and returns it.
        """
        from imageio import imread, imsave
        image=imread(self.path);
        return image;
    
    def label(self):
        """ get the label from the filename. 
            of pattern blabla_label.bla
        """
        # read path
        # get filename
        import os
        fn = os.path.basename(self.path)
        # select .*_(.*)\..*
        import re;
        return re.match(r'.*_(.*)\..*',fn).group(1)

    def process(self):
        """process image with canny edge & hog
            and store value in self.fv
        """
        #init 
        image = self.load();
        
        # to gray ## move to seperate method
        from PIL import Image, ImageEnhance
        from skimage.color import rgb2gray
        import numpy as np
        image=image.copy();    
        image=Image.fromarray(image); # array 2 image
        image = image.convert('L');# 2 gray
        image=np.array(image);


        # canny
        from skimage.feature import canny
        image=canny(image,sigma=2);
        # HOG
        from skimage.feature import hog
        bins=8;
        hpr=10; 
        hog_patch_ratio=(hpr,hpr)
        PPS=D(image.shape,hog_patch_ratio)
        cells_per_block=hog_patch_ratio;# to produce number of bins equal to patches
        fv = hog(image,orientations=bins,cells_per_block=cells_per_block, pixels_per_cell=PPS ,block_norm='L1',transform_sqrt=True)
        self.fv=fv;
        del image;
    @staticmethod    
    def toXy(lazyimages):#not tested yet
        X=[]
        y=[]
        for img in lazyimages:
            X.append(img.fv)
            y.append(img.label())
        return (X,y)
