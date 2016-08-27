# OpenDroneMap-GCP_LIST.TXT-generator

## Technik behind:
Feature Matching + Homography to find Objects (for example GCP_Image_Templates in an ODM image set)
[Learn More](http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html)

## Dependencies
opencv, libopencv-features2d, libopencv-flann, libopencv-nonfree

## Run gcp_txt_gen.py

Simple create an project root directory and place gcp_txt_gen.py, koords.txt in it. inside the project root create "images" directory and "gcp-templates" directory.  

## Create koords.txt
koords text contains your gps coordinates x y z sorted by points.

Example koords.txt
```
WGS84 UTM 39N
P1 631625.6784502362 964921.7122958871 100
P2 631629.4935495785 964967.6482094 100
P3 631696.5718546504,964995.505845105 100
P4 631699.0934857756 964894.2005365156 100
P5 631687.8171783998 964928.6878246851 100
```

