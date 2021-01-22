#import lazyImage
import lazyDataset
#ds=lazyDataset.lazyDataset(path="../../DataSet/EgyptianHieroglyphDataset/Automated/Preprocessed/",save_path="./data/random.pkl",lazy=False)
ds=lazyDataset.lazyDataset(
#        path="../../DataSet/EgyptianHieroglyphDataset/Manual/Preprocessed/",
        save_path="./data/Automated.pkl",
        lazy=True,
        dump=False
        )
result=ds.load()
lazyDataset.summary(result);
s=ds+ds
#print(ds.asDataFrame())
