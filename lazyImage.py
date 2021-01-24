"""
author : Michael

"""
from utils import D;
from pathlib import Path
#~import os
#~import re
#~from imageio import imread, imsave
#import matplotlib.pyplot as plt

#TODO impelement lazyness level to control processing
#TODO? write method 'die' to write label to self.label then clear the path 
#TODO write static method to read list of lazyImages and return (labels, feature vectors )
# path , hog_vector [, label
class Image(object):
    """lazy images
    """
    def __init__(self, path,lazyness=50
            ,labeled_folders=False, func=lambda x : x ):
        self.path=Path(path);
        self.labeled_folders=labeled_folders;
        self.preprocess=func
        self.process();
#        self.label=self.getlabel()

    def load(self):# lazy loading
        """load images when needed and returns it.
        """
        from imageio import imread, imsave
        image=imread(self.path);
        return image;

    def get_folder_name (self,fpath):# needs refactoring
        import os 
        a=os.path.realpath(fpath)
        b=os.path.dirname(a)
        return os.path.basename(b)


    def label(self):
        """ get the label from the filename. 
            of pattern blabla_label.bla
        """
        # read path
        # get filename
        import os
        file_name   = os.path.basename(self.path)
        folder_name = self.get_folder_name(self.path)
        # select .*_(.*)\..*
        import re;
        match=re.match(r'.*_(.*)\..*',file_name)
        if ( self.labeled_folders == True ) :
            return folder_name;
        elif (match == None):
            return folder_name;
        else :
            return match.group(1);

    def process(self):
        """process image with canny edge & hog
            and store value in self.fv
        """
        #init 
        image = self.load();

        # preprocess
#        image = self.preprocess(image);
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
        fv = hog(image,
                orientations=bins
                ,cells_per_block=cells_per_block
                ,pixels_per_cell=PPS 
                ,block_norm='L1'
                ,transform_sqrt=True)
        self.fv=fv;
        del image;
    def plot_gray(self):
        """plot  self in gray """
        import matplotlib.pyplot as plt
        _ , ax1 = plt.subplots(1,1)
        ax1.imshow(self.load(), cmap=plt.cm.gray);
    @staticmethod   # turn into just method 
    def toXy(lazyimages):
        X=[]
        y=[]
        for img in lazyimages:
            X.append(img.fv)
            y.append(img.label())
        return (X,y)
