import os
import lazyImage as li
import pickle
from pathlib import Path
#~ import pandas as pd
#~ from numpy import flip, array

## minor improves
#DONE : make load more os independent 
#DONE : turn this to class with : dump , smart_load
#TODO : imporve to load recursively all images in the dir.
#TODO : update docmuentaion
#DONE : overload + 

## major improve 
#TODO : add handling for a list of paths or one path
#TODO : add drop to drop lables and there data 
#       in __strict_load__ and __lazy_load__
#TODO : overload + to work lazy   

class lazyDataset(object):
    """ lazy reading of dataset set
    """
    def __init__(self
            ,path = "./Dataset/ExampleSet7/train/"
            ,labeled=False
            ,lazy=True
            ,dump=True,save_path=Path("./data/lazyDataset.pkl")
            ,img_class=li.Image):
        """ lazyDataset(...)
        in :(all optional)
            path : images dataset path
            labeled (bool) : if the dataset have folders named 
                        as the label of it's contents.
            save_path : file path to use to load-dump the result.
            lazy : True  : check first if data avilable.
                   False : load and compile dataset.
            dump (bool) :to dump data to save_path or not. 
        ------
        out : use load() to get dataset as (X,y)
        """
# check (strict) *-> load 
#                *-> read -> dump 
        self.path=Path(path)
        self.lazy=lazy
        self.dump=dump
        self.save_path=Path(save_path)
        self.images=[]
        self.img_class=img_class
        self.labeled=labeled

    def load(self):
        if self.lazy == True :
            self.__lazy_load__()
        else :
            self.__strict_load__()
        if self.dump == True :
            self.__dump__()
        return self.images
    
    def __dump__(self):
        pickle.dump(self.images,open(self.save_path, 'wb'))

    def __lazy_load__ (self):
        try :
            self.images=pickle.load(open(self.save_path, 'rb'))
        except:
            self.__strict_load__()

    def __strict_load__(self):
        """ reads dataset strictly
        """
        self.images = scan(
            self.path
            ,img_class=self.img_class
            ,labeled=self.labeled)
    @staticmethod
    def appendXy(Xy1,Xy2):
        X=Xy1[0]+Xy2[0]
        y=Xy1[1]+Xy2[1]
        return (X,y)

    def scan(self,path):
        return scan(
             path
            ,img_class=self.img_class
            ,labeled=self.labeled)


    def asDataFrame(self):
        return toDataFrame(self.load());
    
    def __add__(self,other):
        (X,y)  = self.load()
        (X_,y_)= other.load()
        return (X+X_,y+y_)


def summary(dataset,long=True):
    """
        dataset summary
        in: 
        dataset : (X,y)
        long : (bool) show set of labels
    """
    try :
      X,y=dataset
      y_=set(y)
      print ( "Summary :"
#                  +"\tdata : "+str(len(X))
              +" images : "+str(len(y))
              +"\t uniqe labels: "+str(len(y_)))
      if long : print(str(y_))
    except:
        print ("error input of type : "+str(type(result)))



def pickdrop(T,labels=[]):
    """ in : T : tuple with (X,y)
                where y is lables 
            lables : lables
        out : tuple (ds1,ds2) 
                ds1 : has labels 
                ds2 : rest
    """
    (a,b)=T
    (X,y)=(a.copy(),b.copy())
    (X_,y_)=([],[])
    for l in labels:
        try :
            while(l in y ):
                i= y.index(l)
                y_.append(y[i]);X_.append(X[i])
                del(y[i]);del(X[i])
        except:
            continue
    return ((X_,y_),(X,y))


def drop(T,labels=[]):
    """ in : T : tuple with (X,y)
                where y is lables 
            lables : the lables to be droped
        out : tuple (X,y) without the droped labels
           and it's data
    """
    (a,b)=T
    (X,y)=(a.copy(),b.copy())
    for l in labels:
        try :
            while(l in y ):
                i= y.index(l)
                del(y[i]);del(X[i])
        except:
            continue
    return (X,y)

def pick(T,labels=[]):
    """ in : T : tuple with (X,y)
                where y is lables 
            lables : the lables to be picked
        out : tuple (X,y) with only the picked labels
           and it's data
    """
    (a,b)=T
    (X,y)=(a.copy(),b.copy())
    (X_,y_)=([],[])
    for l in labels:
        try :
            while(l in y ):
                i= y.index(l)
                y_.append(y[i]);X_.append(X[i])
                del(y[i]);del(X[i])
        except:
            continue
    return (X_,y_)

def head_i(T,start=0,i=5):
    """ in : T : tuple with (X,y)
                where y is lables 
    """
    (a,b)=T
    (X,y)=(a.copy(),b.copy())
    (X_,y_)=([],[])
    for n in range(start,i):
        y_.append(y[n]);X_.append(X[n])
        del(y[n]);del(X[n])
    return ((X_,y_),(X,y))



def rename(T,lables=[]):
    pass

def Dumpto(data,fname):
    pickle.dump(data,open(Path(fname), 'wb'))

def toDataFrame(T):
    import pandas as pd
    (X,y)=T
    data = pd.concat(
            [ 
            pd.DataFrame({'label':y}),
                pd.DataFrame(X)
            ],axis=1)
    return data

def concat(one=([],[]),other=([],[])):
    (X,y)  = one
    (X_,y_)= other
    return (X+X_,y+y_)

def sort_max(dataset):
    """ sort max first 
    """
    from numpy import flip, array
    (X,_)=dataset
    X_=[]
    for x in X :
        i=flip(array(x).argsort())
        X_.append(x[i])
    return (X_,dataset[1])

def sorted_alphanumeric(data):
    """
    i/p : data array of strings
    function to sort input in alphanum way 
    to be used in sorting files in write order.
    source : https://stackoverflow.com/a/48030307
    """
    import re
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanumkey = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanumkey)


def safesucc(A,step=-1):
    """ safe sum and default behavoir is to get suc
        A : number
        step : default -1
        result is A if there is error raised from A+step 
    """
    try :
        return A + step
    except:
        return A



def scan(paths,img_class=li.Image,labeled=False
        ,recursive=True,depth=None
        ,sort_func=sorted_alphanumeric):
    """
        scans folder recursively
        in : 
        path : (path/list of paths) to an (image/folder contains images)
        recursive : recursively read 
        depth : level of depth 
                +ve int 

    """
    
    Xys=([],[])
    
    if ( type(paths) == list):
        # how to solve the doublecation 
        for path in paths :
            Xy= scan(path,
                        img_class=img_class,labeled=labeled
                        ,recursive=recursive,depth=depth,sort_func=sort_func)
            Xys=concat(Xys,Xy)
        return Xys
    images=[]

    path=Path(paths)
    try: 
        files=sort_func(os.listdir(path))
    except NotADirectoryError:
        files=[""]# path is an img already

    for file in files: 
        # file is a dir
        if ((path / file).is_dir() and recursive and (depth != 0)) : 
                Xy= scan(path / file,
                        img_class=img_class,labeled=labeled
                        ,recursive=recursive,depth=safesucc(depth),sort_func=sort_func)
                Xys=concat(Xys,Xy)
        # file is file 
        else:    
            try :
                # file is readable img
                images.append(
                    img_class( path / file,labeled_folders=labeled))
            except ValueError:
                # otherwise
                pass
    Xys=concat(Xys , img_class.toXy(images))
    return Xys


