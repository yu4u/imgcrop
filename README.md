# imgcrop
Simple image augmentation library focusing on random geometric cropping.
Different from pipeline-based augmentation libraries, this library efficiently performs cropping and geometric transformations at once.
As image processing functions such as adding Gaussian noise, blurring, and contrast adjustment are not provided,
please use the other great libraries like [imgaug](https://github.com/aleju/imgaug) [1], [Augmentor](https://github.com/mdbloice/Augmentor) [2], and [albumentations](https://github.com/albu/albumentations) [3]
to further transform images cropped by this library.

![](fig/all1.png?raw=true)

## Features

- Simple API, easy to use
- Efficient; cropping and all geometric transformations are performed at once (by a single perspective transformation)
- Guarantee that all pixels in cropped image are taken from inside the original image (if margin is not used)


## Installation

```bash
pip install imgcrop
```

## APIs

### imgcrop.get_cropper
```python
get_cropper(patch_size=128, scale=(1.0, 1.0), rotate=(0, 0), distort=0.0, flip=0.0, margin=0)
```

#### parameters
- **patch_size**: *int, default 128*
  - output patch size (in pixel)
- **scale**: *tuple of float, default (1.0, 1.0)*
  - sampling scale range
- **rotate**: *tuple of int, default (0, 0)*
  - sampling rotation range (in degree)
- **distort**: *float, default 0.0*
  - distortion strength in perspective transformation (ratio to output image scale)
- **flip**: *float, default 0.0*
  - horizontal flip probability
- **margin**: *int, default 0*
  - margin in cropping around original image

#### returns
- **random_crop**: function


### random_crop
```python
random_crop(img, points=None) -> cropped_img[, output_points], src_points, m
```

#### parameters
- **img**: *numpy array (single image) or list of numpy arrays (multiple images)*
  - input image(s) to be cropped with the same geometric transformation
- **points**: *numpy array with the shape (point_num, 2), default None*
  - input points to be transformed with the same transformation matrix as input image(s)

#### returns
- **cropped_img**: *numpy array or list of numpy arrays)*
  - cropped output image(s)
- **output_points**: *numpy array with the shape (point_num, 2)*
  - output points if input points are given
- **src_points**: *numpy array*
  - points defining the cropped region in the input image(s)
- **m**: *numpy array*
  - 3x3 perspective transformation matrix from the input image(s) to the output image(s)

## Example

Pleaes run or refer to [the example script](example/example.py) to see how this library works:

```bash
python example/example.py
```

You can easily try different parameters by arguments:

```bash
optional arguments:
  -h, --help            show this help message and exit
  --patch_size PATCH_SIZE
                        output patch image size (default: 256)
  --scale SCALE SCALE   scale range in sampling (default: [0.8, 1.2])
  --rotate ROTATE ROTATE
                        rotation range in sampling (default: [-60, 60])
  --distort DISTORT     distortion strength for perspective transformation
                        (default: 0.2)
  --flip FLIP           horizontal flip probability (default: 0.5)
  --margin MARGIN       margin around original image (default: 0)
```

| parameters | cropping results (input, cropped, mask, keypoints) |
| --- | --- |
| scaling | ![](fig/scale1.png?raw=true) |
|  | ![](fig/scale2.png?raw=true) |
|  | ![](fig/scale3.png?raw=true) |
| rotation + scaling | ![](fig/rotate1.png?raw=true) |
|  | ![](fig/rotate2.png?raw=true) |
|  | ![](fig/rotate3.png?raw=true) |
| distortion + scaling | ![](fig/distort1.png?raw=true) |
|  | ![](fig/distort2.png?raw=true) |
|  | ![](fig/distort3.png?raw=true) |
| flip + rotation | ![](fig/flip1.png?raw=true) |
|  | ![](fig/flip2.png?raw=true) |
|  | ![](fig/flip3.png?raw=true) |
| margin + scaling | ![](fig/margin1.png?raw=true) |
|  | ![](fig/margin2.png?raw=true) |
|  | ![](fig/margin3.png?raw=true) |
| all | ![](fig/all1.png?raw=true) |
|  | ![](fig/all2.png?raw=true) |
|  | ![](fig/all3.png?raw=true) |

## Algorithm
Patch region in the original image is defined by a set of four points.
These points are randomly transformed according to transformation parameters.
The transformation matrix from input image to output image is then calculated using these points.
Finally, cropping is performed by applying perspective transformation.

![](fig/algorithm.png?raw=true)

## References
1. imgaug, https://github.com/aleju/imgaug
2. Augmentor, https://github.com/mdbloice/Augmentor
3. albumentations, https://github.com/albu/albumentations
