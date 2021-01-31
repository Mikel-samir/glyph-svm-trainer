## Dependencies
  ### Python packages
  all of them comes with anaconda installer.
  * [**imageio**](https://anaconda.org/menpo/imageio)
  * [**pillow**](https://anaconda.org/anaconda/pillow)
  * pickle
  * pandas
  * numpy
  * sklearn
  * skimage
  * matplotlib

  ### directory hierarchy

  * model
      * [**Main.pkl**](https://drive.google.com/file/d/1ISCgNbj8F-lXHeVAF1LYiTLNcvvO4p9G/view?usp=sharing) | the svm model
  * data
      * Main.pkl | the data set in case of need for training


# svm-trainer
## how to use ?
1. load a model
2. prepare image(s)
	1. load image from path
	2. load image from (numpy array / PIL.Image / ..) 
3. predict the image(s)'s label


### load a model 
load a compiled model from model file.

**Note:** remember to change path to windows version with \ instead of /


```python
import lazyModel
model=lazyModel.lazyModel(
        save_path="./model/Main.pkl"
        )
model.load()

```

### prepare image(s)

#### load image from path


```python
import lazyImage as li
# anypath for example image in data set
image=li.Image("./Dataset/Automated/Preprocessed/3/030000_D35.png").toX()
```

#### load image from (numpy array / PIL.Image / ..) 


```python
from skimage import data
import lazyImage as li
# example image in a numpy array 
img = data.astronaut()
```


   ![png](https://i.imgur.com/OoYfutH.png)



```python
import lazyImage as li

# image 
image_numpy=li.Image.FromObj(img).run().toX()

# images
imgs=[img,img,img]
images=li.Image.FromObjs(imgs)
images=li.Image.runAll(images)
images=li.toX(images)
```

### predict the image(s)'s label


```python
model.Predict(image)
# out :
# label , probabilty
```




    out : [('D35', 0.3216917080504977)]




```python
model.Predict(images)
```
    out:   [('F31', 0.03261634682111355),
          ('F31', 0.03261634682111355),
          ('F31', 0.03261634682111355)]


