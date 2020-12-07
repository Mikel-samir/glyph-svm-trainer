#import lazyImage
import lazyImage 
import pickle

I=pickle.load( open("./data/lazyDataset.ss", 'rb'))
toXy=lazyImage.Image.toXy
X,y=toXy(I)
print (str(y))
