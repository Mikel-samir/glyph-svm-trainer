import os
import lazyImage as li
#TODO : make load more os independent 
#TODO : write one that uses lazyImage.label instead of dir name.
def load(path = "/home/loxymondor/docs/facu/Gproj/Proj/DataSet/EgyptianHieroglyphDataset/ExampleSet7/train/",seprator="/",Random=False):
        """ load (path,seprator)
        this method assumes that each folder name is the lable of the images it contains.
        path : is dir of dataset
                must end with a seprator 
                example : /home/s/d/ is right
                          /home/s/d is wrong

        seprator : is the os seprator 
                linux -> /
                win   -> \\
        out : (X,y) 
                X -> feature vector array
                y -> label for each corresponding feature vector
        """
        images = []
        labels = []
        root= os.listdir(path) #list of directory files

        for label in root :
            if os.path.isdir(path+label): 
                imgs=os.listdir(path+label)
#                print("\t"+label)
                for img in imgs: 
                    #li.Image(path+"/"+label+"/"+img)
                    limg=li.Image(path+seprator+label+seprator+img)
                    images.append(limg.fv)
                    labels.append( limg.label() if Random else label)
#                    print (img)
        return (images,labels)
