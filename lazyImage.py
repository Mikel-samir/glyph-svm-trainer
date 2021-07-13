"""
author : Michael

"""
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
    def __init__(self, path,
                lazyness=50,standard_size=(75,50),
                labeled_folders=False, func=lambda x : x,auto_proc=True):
        """
           path : path to an image.
           standard_size : size to resize to default (75,50) if None no resize
        """
        self.path=Path(path);
        self.labeled_folders=labeled_folders;
        self.standard_size=standard_size
#        self.preprocess=func
        if (auto_proc == True):
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
            # folder name
            return folder_name
        elif (not(self.labeled_folders) and (match!=None)) :
            # label
            return match.group(1);
        elif (not(self.labeled_folders)) :
            # name without extension
            return re.match(r'(.*)\..*',file_name).group(1)
        elif (not(self.labeled_folders)):
            # all file name not used yet
            return file_name
        else:
            return folder_name

    def process(self):
        """process image with edge detection & hog
            and store value in self.fv
        """
        #init 
        image = self.load();

        # preprocess
        # to gray ## move to seperate method
        from PIL import Image, ImageEnhance
        from skimage.color import rgb2gray
        import numpy as np
        image=np.array(image)
        image=image.copy();    
        image=Image.fromarray(image); # array 2 image
        image=image.convert('L');# 2 gray
        if self.standard_size != None : 
            image=image.resize((self.standard_size[1],self.standard_size[0])) ; # resize
        image=np.array(image);


        # 
        from skimage.filters import sobel
        image=sobel(image);

        # HOG
        # shape (75,50)
        #  [3, 5, 5]
        #  [2, 5, 5]
        
        from skimage.feature import hog
        bins=8;
        hpr=10; 
        hog_patch_ratio=(hpr,hpr);
        PPS=D(image.shape,hog_patch_ratio);# (7.5,5)
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
    
    def toX(self):
        return toX([self])[0]
    
    @staticmethod
    def FromObj(img):
        """ turns numpy/Image image into lazyImage
        """
        out=Image("",auto_proc=False)
        out.load=lambda : img
        return out
    def run(self):
        self.process()
        return self
    @staticmethod
    def FromObjs(imgList):
        """ turns numpy/Image images into lazyImage list
        """
        out=[]
        for img in imgList :
            out.append(Image.FromObj(img))
        return out
    @staticmethod
    def runAll(limgs):
        for limg in limgs:
            limg.run()
        return limgs

def toX(lazyimages):
    X=[]
    for img in lazyimages:
        X.append(img.fv)
    return X

def D(I , N ): 
        """ get no. of pixels to divide image with size I <tuple> to N[0]xN[1] <tuple> 
            @unsafe  : produce float no.
        """ 
        return (I[0]/N[0],I[1]/N[1])
