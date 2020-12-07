#import lazyImage
import Dataset
X,y=Dataset.load(path="../../DataSet/EgyptianHieroglyphDataset/Automated/Preprocessed/",Random=True)
print ("Done ! :)\n"+str(len(X))+"\t"+str(len(y))+"\nlabels: \n"+str(y))
