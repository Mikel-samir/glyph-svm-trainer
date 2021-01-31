# svm-trainer
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
    * [**Main.pkl**]() | the svm model
* data
    * Main.pkl | the data set in case of need for training 

## how to use ?
1. load a model
2. prepare image(s)
	1. load image from path
	2. load image from object image (numpy array / PIL.Image / ..) 
3. predict the image(s)'s label

### load a model 
load a compiled model from model directory.

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
image=li.toXy(li.Image("path/to/image.jpg"))
```

#### load image from object image (numpy array / PIL.Image / ..) 

```python
import lazyImage as li
# assuming that img is a numpy array 

# image 
image=li.Image.FromObj(img).run()

# images
# assuming imgs is list
images=li.Image.FromObjs(imgs)
images=li.Image.runAll(images)
```

### predict the image(s)'s label

```python
result=model.Predict(image)
# output :
# p -> probability 
# ('label',p)
results=model.Predict(images)
# output : 
# [(l,p),(l,p),...]
```

#### what's next ? 


**see : demo.py**
