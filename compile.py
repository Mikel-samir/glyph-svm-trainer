#import lazyImage
import lazyDataset
import lazyModel
from pathlib import Path
import argparse

import time
"""
# Generates the Dataset & the Model

* Dataset root directory in same dir and named `Dataset`
* compiled dataset will be generated in ./data/ dir
* saves model in ./model/ dir

"""

parser = argparse.ArgumentParser()
parser.add_argument("-S"
                    ,"--not-safe"
                    , help="set All the safety_lock to off to do strict loading."
                    ,action="store_false")
parser.add_argument("-M"
                    ,"--model-not-safe"
                    , help="set the model's to off to do strict loading."
                    ,action="store_false")

parser.add_argument("-T"
                    ,"--test"
                    , help="do splitting & testing.."
                    ,action="store_true")


parser.add_argument("-e"
                    ,"--ext"
                    ,help="set an extension."
                    ,type=str,nargs=1,default=[""])
args = parser.parse_args()


safety_lock=args.not_safe;# to stop strict loading if true
model_safety_lock=args.model_not_safe;# to stop strict loading if true
testing_lock=args.test;# to stop strict loading if true
ext=args.ext[0]

data = Path("./data/")
dataset = Path("./Dataset")
model = Path("./model/")
#folder="Preprocessed"
folder="Raw"

print ("loading dataset ...")
start_time=time.monotonic() 
# Manual
dsM=lazyDataset.lazyDataset(
        path= dataset /"Manual"/ folder ,
        save_path=data / str('Manual'+ext+'.pkl'),
        lazy=safety_lock
        )

# Automated
dsA=lazyDataset.lazyDataset(
        path= dataset /"Automated"/ folder ,
        save_path=data / str('Automated'+ext+'.pkl'),
        lazy=safety_lock
        )

# All Dataset
ds=dsA+dsM
lazyDataset.Dumpto(ds,data /str('All'+ext+'.pkl'))
#print("pure:\n")
#lazyDataset.summary(ds)

# filtered Dataset
ds=lazyDataset.drop(ds,labels=['UNKNOWN'])
lazyDataset.Dumpto(ds,data / str('Main'+ext+'.pkl'))
#print("filtered:\n")

start_time-=time.monotonic()
print ("dataset is loaded in "+str(abs(start_time))+" sec ...")
lazyDataset.summary(ds,long=False)
#lazyDataset.summary(ds)

# Model
## training
if testing_lock :
    train,test=lazyModel.split(ds)
    # picking labels that's in the dataset
    _,ya=train
    _,yb=test
    yi=set(yb).intersection(ya)
    test,rest=lazyDataset.pickdrop(test,labels=list(yi))
    ds=lazyDataset.concat(ds,rest)

    

a=lazyModel.lazyModel(
        dataset=ds,
        save_path= model / str('Main.proba'+ext+'.pkl')
        ,lazy=(safety_lock and model_safety_lock)
        )
start_time=time.monotonic()
print ("loading the model ...")
a.load()
start_time-=time.monotonic()
print ("the model loaded in "+str(abs(start_time))+" sec ...")
## testing
if testing_lock :
    print ("testing the model ...")
    start_time=time.monotonic()
#    print ("testing labels :"+str(yi))
    a.test(test)
    start_time-=time.monotonic()
    print ("the model is tested in "+str(abs(start_time))+" sec ...")

    start_time=time.monotonic()
    a.train(test)
    start_time-=time.monotonic()
    print ("the model final training done in "+str(abs(start_time))+" sec ...")


