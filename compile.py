#import lazyImage
import lazyDataset
import lazyModel
from pathlib import Path
"""
# Generates the Dataset & the Model

* Dataset root directory in same dir and named `Dataset`
* compiled dataset will be generated in ./data/ dir
* saves model in ./model/ dir

"""
safety_lock=True;# to stop strict loading if true

data = Path("./data/")
dataset = Path("./Dataset")
model = Path("./model/")
ext=''

# Manual
dsM=lazyDataset.lazyDataset(
        path= dataset /"Manual"/"Preprocessed" ,
        save_path=data / str('Manual.Raw'+ext+'.pkl'),
        lazy=safety_lock
        )

# Automated
dsA=lazyDataset.lazyDataset(
        path= dataset /"Automated"/"Preprocessed" ,
        save_path=data / str('Automated.Raw'+ext+'.pkl'),
        lazy=safety_lock
        )

# All Dataset
test=dsA+dsM
lazyDataset.Dumpto(test,data /str('All'+ext+'.pkl'))
print("pure:\n")
lazyDataset.summary(test)

# filtered Dataset
test=lazyDataset.drop(test,labels=['UNKNOWN'])
lazyDataset.Dumpto(test,data / str('Main'+ext+'.pkl'))
print("filtered:\n")
lazyDataset.summary(test)


# Model
## training
X,y=test
a=lazyModel.lazyModel(
        dataset=(X,y),
        save_path= model / str('Main.proba'+ext+'.pkl')
        ,lazy=safety_lock
        )
a.load()
## testing
a.__test__(X,y)



