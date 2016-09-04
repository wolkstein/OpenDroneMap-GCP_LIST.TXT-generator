# OpenDroneMap-GCP_LIST.TXT-generator

Create GCP_List.txt files from a ODM Data Set with more than 100 images is an painstaking task. This Python Script will do this task for you.

This repository contains some example data stored in "Images", "gcp -templates" and coords.txt. The images inside "images" are not a full usable ODM Data Set. There are only a few images to test successfully the functionality of this script.

## Technik behind:
Feature Matching + Homography to find Objects (for example GCP_Image_Templates in an ODM image set)
[Learn More](http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html)

## Dependencies
opencv, libopencv-flann, libopencv-nonfree
Optinal for Qr-Code template compare install zbar-tools

# Run gcp_txt_gen.py

Simple create an project root directory and place gcp_txt_gen.py and coords.txt in it. Inside the project root create "images" directory and "gcp-templates" directory.  

## Create coords.txt
coords.txt contains your gps coordinates x y z sorted by points.

Example coords.txt
```
WGS84 UTM 32N
P1: 481367 5782936 100
P2: 481396 5782940 100
P3: 481413 5783008 100
P4: 481350 5783011 100
P5: 481372 5782999 100
```
First row contains the coordinate system. 
Following rows for GCP's starts with the number of Control Point "P1: "- "Pn: " followed by  X, Y & Z coordinate in your coordinate system. whitespace separate the coords items.

## Create GCP_Template_Images
Important! We need Templates from the Current ODM Image-Set we plan to process. 
Open with Gimp some of your ODM-Dataset-Images which contains GCP's we are looking for.
With the rectangle selection tool select an area with the GCP. The mesure point must be in the center. Gimp rectangle selection offers option you can enable to draw the selection from center. See Image 1. The selected area need a size around 100x100 px. It is not important if the area is a little bit bigger than your gcp plane. Also the orientation of the GCP is not important. It is only important that the diagonal from the selection-corners will cross exactly the gps measure point from your GCP.

Create an new image from selection. See Image 2. And save the image with numbered names according to the order of our GCP 's.
For example GCP 1 to P01.jpg, GCP 2 to P02.jpg and so on.
Caution , to avoid errors in the sorting of GCP template images. If they have more than 10 GCP template images and less than 100 GCP template images they use the image name P01 - P99 . If you use more than 100 GCP template images , they have the image name P001 - P999 .

Save all GCP template images inside your your gcp-templates directory.

Gimp Selection Tool
![Image 1](https://github.com/wolkstein/OpenDroneMap-GCP_LIST.TXT-generator/raw/master/doc/CREATE_GCP_TEMPLATE_GIMP_1.jpg "Make GCP selection")

Gimp, create new image from selection
![Image2](https://github.com/wolkstein/OpenDroneMap-GCP_LIST.TXT-generator/raw/master/doc/CREATE_GCP_TEMPLATE_GIMP_2.jpg "Create new image from selection")

# Start Script
Now you can run the script.
Option -d enable debug output. This will additionally create an DEBUG-GCP_LIST.txt file. In this file at the beginning of each row you can find the GCP Nr. P1 - Pn. This will help you to check images if we really find the right positions. Option --min_match_count is default at 12. 
```
usage: gcp_txt_gen.py [-h] [-d] [-q] [--min_match_count MIN_MATCH_COUNT]
                      [-f FIRST_GCP_POINT] [-i IGNORE_BORDER]

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Will additionally create an DEBUG-GCP_LIST.txt file
                        with Pointnames P1 - Pn in each row
  -q, --qr_code_compare
                        compare QR-Code in GCP matches against the QR Code
                        from Template QR-Code based GCP. This needs QR Code
                        based GCPs
  --min_match_count MIN_MATCH_COUNT
                        min_match_count "Default = 12, Min = 4" set the
                        minimum amount of required good keypoints to accept a
                        match of Template in Image
  -f FIRST_GCP_POINT, --first_gcp_point FIRST_GCP_POINT
                        GCP Point start from [n] number
  -i IGNORE_BORDER, --ignore_border IGNORE_BORDER
                        Ignore GCP Point inside Image Border [px].


```
If the script finished successfully you get an nice gcp_list.txt file in working directory.
copy this in your ODM working directory and star ODM with  --odm_georeferencing-useGcp.

