#import lazyImage
import lazyDataset
import lazyModel
from pathlib import Path

data = Path("./data")
ds=lazyDataset.lazyDataset(
        save_path=data / 'Main.pkl',
#        lazy=False,
        dump=False
        )
X,y=ds.load()
#lazyDataset.summary((X,y));
a=lazyModel.lazyModel(
#        dataset=(X,y),
        save_path="./model/Main.proba.pkl"
        )
a.load()
#test= (X[0:100],y[0:100])
#a.__test__(test[0],test[1])
x=200
res=a.Predict(X[0:x])
for i in range(x):
    print (str(res[i][0]==y[i])+"\t"+str(res[i])+"\t"+str(y[i]))
