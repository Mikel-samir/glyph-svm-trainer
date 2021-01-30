#import lazyImage
import lazyDataset
import lazyModel
from pathlib import Path

data = Path("./data")
dsM=lazyDataset.lazyDataset(
        path="./Dataset/Manual/Raw/" ,
        save_path=data / 'Manual.Raw.pkl',
        )
dsA=lazyDataset.lazyDataset(
        path="./Dataset/Automated/Raw/" ,
        save_path=data / 'Manual.Raw.pkl',
        )
#lazyDataset.summary((X,y));
a=lazyModel.lazyModel(
#        dataset=(X,y),
        save_path="./model/Main.proba.pkl"
        )
a.load()

test=dsA+dsM
lazyDataset.Dumpto(test,'./data/All.Raw.pkl')
print("pure:\n")
lazyDataset.summary(test)
test=lazyDataset.drop(test,labels=['UNKNOWN'])
lazyDataset.Dumpto(test,'./data/Main.Raw.pkl')
print("filtered:\n")
lazyDataset.summary(test)
X,y=test
a.__test__(X,y)

#x=200
#res=a.Predict(X[0:x])
#for i in range(x):
#    print (str(res[i][0]==y[i])+"\t"+str(res[i])+"\t"+str(y[i]))
