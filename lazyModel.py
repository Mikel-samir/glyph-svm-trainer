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
             split     : (bool) split dataset ? 

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


    def __get_dataset__():
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

    def __split__(self):
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


def evaluate(y_test,y_pred):
    """ classification report
    """
    from sklearn.metrics import  accuracy_score,classification_report
    print("classification report :")
    print(classification_report(y_test,y_pred))
    print("Accuracy:",accuracy_score(y_test, y_pred))
