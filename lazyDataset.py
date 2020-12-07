import os
import lazyImage as li
#TODO : make load more os independent 
#TODO turn this to class with : dump , smart_load
def load(path = "/home/loxymondor/docs/facu/Gproj/Proj/DataSet/EgyptianHieroglyphDataset/ExampleSet7/train/",seprator="/",Random=False, save="",smart=False):
        """ load (path,seprator)
        this method assumes that each folder name is the lable of the images it contains.
        path : is dir of dataset
                must end with a seprator 
                example : /home/s/d/ is right
                          /home/s/d is wrong

        seprator : is the os seprator 
                linux -> /
                win   -> \\
        ## not implemented
        save_dir : use to load-dump the result
        smart : to check if dataset is dumped so read it instead of compiling .

        ------
        out : lazyImage array
        """
        images = []
        root= os.listdir(path) #list of directory files

        for label in root :
            if os.path.isdir(path+label): 
                imgs=os.listdir(path+label)
#                print("\t"+label)
                for img in imgs: 
                    #li.Image(path+"/"+label+"/"+img)
                    images.append(li.Image(path+seprator+label+seprator+img))
#                    print (img)

#        import pickle
#        images=pickle.load( open("./data/lazyDataset.ss", 'rb'))
#        if save_dir != "" :
#           pickle.dump(images, open(save_dir, 'wb'))
        return images
