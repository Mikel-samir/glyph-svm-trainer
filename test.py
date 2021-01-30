#import lazyImage
import lazyDataset
import lazyModel
from pathlib import Path

data = Path("./data")
ds=lazyDataset.lazyDataset(
        path="./Dataset/Manual/Raw/" ,
        save_path=data / 'test_resize.pkl',
        lazy=False,
        dump=False
        )
#lazyDataset.summary((X,y));
a=lazyModel.lazyModel(
#        dataset=(X,y),
        save_path="./model/Main.proba.pkl"
        )
a.load()

test=ds.load()
test=lazyDataset.drop(test,labels=['UNKNOWN'])
X,y=test
a.__test__(X,y)

#x=200
#res=a.Predict(X[0:x])
#for i in range(x):
#    print (str(res[i][0]==y[i])+"\t"+str(res[i])+"\t"+str(y[i]))
