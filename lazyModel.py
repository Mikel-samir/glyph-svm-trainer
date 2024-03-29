from sklearn.svm import SVC
import pickle
import warnings
#~ from sklearn.model_selection import train_test_split 
#~ from lazyImage import lazyImage 
import lazyDataset
from pathlib import Path

# TODO : train with all data .

class lazyModel(object):
    """ lazy model train trainer
    """
    def __init__(self,
            model=SVC(probability=True),
            dataset=None,
            save_path="./model/Main.pkl",
            lazy=True,dump=True,
            split=False):
        """
        in : model     : model object
             dataset   : tuple or lazyDataset object.
             save_path : path to save/load model
             lazy      : 
             dump      :
             split     : (bool) split dataset ?(disabled) 

        out :
        """
        self.save_path=Path(save_path);
        self.lazy=lazy;
        self.dump=dump;
        self.dataset=dataset;
        self.model=model;

    def __train__(self):
        if self.dataset == None :
            (X,y)=self.__get_dataset__()
        else :
            if type(self.dataset) == tuple :
                (X,y)=self.dataset;
            else :
                (X,y)=self.dataset.load();
        

#        if self.split == True : 
#            (X_test,y_test)=self.__split__()
#            ()
        
        # training
        warnings.warn("training the model ...")
        self.model.fit(X,y)
        self.__dump__()
#        if self.split == True : 
#            warnings.warn("testting the model ...")
#            self.__test__(X_test,y_test)

    def train(self,Xy):
        self.dataset=Xy
        self.__train__()

    @staticmethod
    def __get_dataset__():
        raise(ValueError("no dataset is given"))
        warnings.warn("Dataset lazy loading failed, strict loading will be used.",RuntimeWarning)
        ## preparing paths
        datapath=Path("./data/")
        Mpath=datapath / "Manual.pkl"
        Apath=datapath / "Automated.pkl"
        dspath=Path("./Dataset/")
        Mpath_= dspath / 'Manual'/ 'Preprocessed'
        Mpath_= dspath / 'Automated'/ 'Preprocessed'

        # reading datasets
        datasetM=lazyDataset.lazyDataset(save_path=M).load()
        datasetA=lazyDataset.lazyDataset(save_path=lazyA).load()
        dataset=datasetA+datasetM
        del(datasetA);del(datasetM)
        dataset=lazyDataset.drop(dataset,labels=['UNKNOWN'])
        return dataset
    
    def __split_td__(self):
        """ split dataset to test/dev/train
        """
        (X,y)=self.dataset
        from sklearn.model_selection import train_test_split
        # 70% training and 30% test+dev
        X_train, X_test_, y_train, y_test_ = train_test_split(X, y, test_size=0.3, random_state=1);
        # 2/3 dev , 1/3 test
        X_dev, X_test , y_dev, y_test  = train_test_split(X, y, test_size=1/3, random_state=1); 
        name=self.__get_name__()
        lazyDataset.Dumpto((X_dev,y_dev),Path('./data/'+name+'.dev.pkl'))
        lazyDataset.Dumpto((X_test,y_test),Path('./data/'+name+'.test.pkl'))
        self.dataset=(X_train,y_train)
        return (X_test,y_test)

    def __get_name__(self):
        return self.save_path.stem


    def __test__(self,X,y_test):
        y_pred=self.model.predict(X)
        evaluate(y_test,y_pred)

    def report(self):
        pass
    
    def Predict(self,glys):
        """
        """
        import numpy as np
        clf=self.model
        X=[]
        if type(glys) == np.ndarray and len(glys.shape) == 1 :
            glys=[glys]
        if type(glys) == list :
            P=clf.predict_proba(glys)
            for p_ in P : 
                pm=p_.argmax()
                X.append((clf.classes_[pm],p_[pm]))
        return X
    
    def test(self,X,y):
        self.__test__(X,y)
    
    def test(self,Xy):
        self.__test__(Xy[0],Xy[1])


    def load(self):
        if self.lazy == True :
            self.__lazy_load__()
        else :
            self.__strict_load__()

    def __strict_load__(self):
        warnings.warn("lazy loading failed, strict loading will be used.",RuntimeWarning)
        self.__train__();

    def __lazy_load__ (self):
        try :
            self.model=pickle.load(open(self.save_path, 'rb'))
        except:
            self.__strict_load__()

    def __dump__(self,lock=None):
        if lock == True or self.dump == True :
            pickle.dump(self.model,open(self.save_path, 'wb'))
    def dump():
        self.__dump__(lock=True)

def split (Xy,test_size=0.3):
    """spilt a given dataset
        in: 
         Xy : (X,y) dataset
         test_size :
    """
    (X,y)=Xy
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=1);
    Xy_train =(X_train,y_train)
    Xy_test =(X_test,y_test)
    return (Xy_train,Xy_test)


def faire_split(Xy,size=0.3,limit=5):
    """ split & take into considration that test data is in train data
        limit : +ve or -ve for infinite
    """
    from math import ceil
    expected_size=ceil(len(Xy[0])*size)
    yb=[]
    rest=([],[])
    test=rest
    train=Xy
    while((len(yb)<=expected_size) and (limit > 0)):
        train,test_=split(train)
        test=lazyDataset.concat(test,test_)
        # picking labels that's in the dataset
        _,ya=train
        _,yb=test
        yi=set(yb).intersection(ya)
        test,R=lazyDataset.pickdrop(test,labels=list(yi))
        rest=lazyDataset.concat(rest,R)
        limit-=1
    train=lazyDataset.concat(train,rest)
    d=len(test[0])-expected_size
    if (d > 0):
        train_,test=lazyDataset.head_i(test,i=d)
        train=lazyDataset.concat(train,train_)

    # test is so big ?
    return (train,test)


def evaluate(y_test,y_pred):
    """ classification report
    """
    from sklearn.metrics import  accuracy_score,classification_report,log_loss
    print("classification report :")
    print(classification_report(y_test,y_pred))
    print("Accuracy:",accuracy_score(y_test, y_pred))
#    print("logloss:",log_loss(y_test, y_pred))


from typing import List , Tuple,Any
Predictions=List[Tuple[str,Any]]

def print_pred(pred: Predictions) -> str:
    out=[]
    for i in pred :
        out.append(i[0])
    return ",".join(out)

def parse_pred(String: str,holder=0.5) -> Predictions :
    import re
    match=re.findall(r'((Aa|Ff|N[UL]|[A-Z])\d{1,4})',String)
    out=[]
    for m in match:
            out.append((m[0],holder))
    return out


class Timer(object):
    def __init__(self):
        """
            time in milli second
        """
        from time import monotonic,monotonic_ns
        self.start_time=0
        self.end_time=0
        self.diff=0
        self.clock=monotonic_ns 


    def start(self):
        self.start_time=self.clock()

    def end(self):
        self.end_time=self.clock()
        self.diff=((self.end_time)-(self.start_time))*(10**-6)


