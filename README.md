# svm-trainer
## Dependencies

* **imageio**
* pickle
* pandas
* numpy
* pillow 
* sklearn
* skimage
* matplotlib.pyplot

## how to use ?
1. load a model
2. prepare image(s)
	1. load image from path
	2. load image from (numpy array / PIL.Image / ..) 
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
image=li.Image("path/to/image.jpg")
```

#### load image from (numpy array / PIL.Image / ..) 

```python
import lazyImage as li
# assuming that img is a numpy array 

# image 
image=li.Image.FromObj(img).run()

# images
images=li.Image.FromObjs(imgs)
images=li.Image.runAll()
```

### predict the image(s)'s label


```python
result=model.Predict(image)
# output :
# p -> probability 
# ('label',p)
results=model.Predict(images)

```
