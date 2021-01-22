#import lazyImage
import lazyDataset
import lazyModel
from pathlib import Path

data = Path("./data")
ds=lazyDataset.lazyDataset(
#        path="./DataSet/Manual/Preprocessed/",
#        path='./Dataset/Manual/Preprocessed/',
        save_path=data / 'Main.pkl',
        lazy=False,
        dump=False
        )
#result=ds.load()
#lazyDataset.summary(result);
test= lazyDataset.lazyDataset(save_path='data/model.dev.pkl')+lazyDataset.lazyDataset(save_path='data/model.test.pkl')
a=lazyModel.lazyModel(dataset=ds)
a.load()
a.__test__(test[0],test[1])
