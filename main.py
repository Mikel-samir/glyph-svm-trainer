#import lazyImage
import lazyDataset
from pathlib import Path

data = Path("./data")
ds=lazyDataset.lazyDataset(
#        path="./DataSet/Manual/Preprocessed/",
        path='./Dataset/Manual/Preprocessed/',
        save_path=data / 'test_.pkl',
        lazy=False,
        dump=False
        )
result=ds.load()
lazyDataset.summary(result);
