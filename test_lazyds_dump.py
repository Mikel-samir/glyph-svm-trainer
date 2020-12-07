#import lazyImage
import lazyDataset as Dataset
import pickle

I=Dataset.load(path="../../DataSet/EgyptianHieroglyphDataset/Automated/Preprocessed/",Random=True)
pickle.dump(I, open("./data/lazyDataset.ss", 'wb'))
