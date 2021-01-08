#import lazyImage
import lazyDataset
ds=lazyDataset.lazyDataset(path="../../DataSet/EgyptianHieroglyphDataset/Automated/Preprocessed/",save_path="./data/random.pkl",lazy=False)
result=ds.load()
try :
 X,y=result
 print ("Done ! :)\n"+str(len(X))+"\t"+str(len(y))+"\nlabels: \n"+str(set(y)))
except:
    print (str(type(result)))
