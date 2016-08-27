# OpenDroneMap-GCP_LIST.TXT-generator

## Technik behind:
Feature Matching + Homography to find Objects (for example GCP_Image_Templates in an ODM image set)
[Learn More](http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html)

## Dependencies
opencv, libopencv-features2d, libopencv-flann, libopencv-nonfree

# Run gcp_txt_gen.py

Simple create an project root directory and place gcp_txt_gen.py and koords.txt in it. Inside the project root create "images" directory and "gcp-templates" directory.  

## Create koords.txt
koords.txt contains your gps coordinates x y z sorted by points.

Example koords.txt
```
WGS84 UTM 39N
P1 631625.6784502362 964921.7122958871 100
P2 631629.4935495785 964967.6482094 100
P3 631696.5718546504,964995.505845105 100
P4 631699.0934857756 964894.2005365156 100
P5 631687.8171783998 964928.6878246851 100
```
First row contains the coordinate system. 
Following rows for GCP's starts with the number of Control Point "P1 t- Pn" followed by  X, Y & Z coordinate in your coordinate system. whitespace separate the items.

## Create GCP_Template_Images
Important! We need Templates from the Current ODM Image-Set we plan to process. 
Open with Gimp some of your ODM-Dataset-Images which contains GCP's we are looking for.
With the rectangle selection tool select an area with the GCP. The mesure point must be in the center. Gimp rectangle selection offers option you can enable to draw the selection from center. See Image 1. The selected area need a size around 100x100 px. It is not important if the area is a little bit bigger than your gcp plane. Also the orientation of the GCP is not important. It is only important the the diagonal from the selection-corners will cross exactly the gps measure point from your GCP.

Create an new image from selection. See Image 2. And save the image with a name corresponding to the GCP Point Number.
GCP 1 to P1.jpg, GCP 2 to P2.jpg and so on. P1.jpg, P2.jpg... must corresponding witch the P1, P2.... in koords.txt!

Gimp Selection Tool
![Image 1](https://github.com/wolkstein/OpenDroneMap-GCP_LIST.TXT-generator/raw/master/doc/CREATE_GCP_TEMPLATE_GIMP_1.jpg "Make GCP selection")

Gimp, create new image from selection
![Image2](https://github.com/wolkstein/OpenDroneMap-GCP_LIST.TXT-generator/raw/master/doc/CREATE_GCP_TEMPLATE_GIMP_2.jpg "Create new image from selection")

