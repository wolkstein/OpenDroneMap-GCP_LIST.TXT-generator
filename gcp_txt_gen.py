import numpy as np
import cv2
import argparse
import glob


# ---Helper---
def roundTraditional(val,digits):
   return round(val+10**(-len(str(val))-1))
# ---~Helper---

GCP_DEBUGMODE = False
MIN_MATCH_COUNT = 12

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', required=False , help='Will create an GCP_LIST.txt file with Pointnames P1 - Pn in each row')
parser.add_argument('--min_match_count', type=int, default=12, required=False, help='min_match_count "Default = 12, Min = 4" set the minimum amount of required good keypoints to accept a match of Template in Image')
args = parser.parse_args()

MIN_MATCH_COUNT = args.min_match_count
if MIN_MATCH_COUNT < 4:
    MIN_MATCH_COUNT = 4
#print MIN_MATCH_COUNT

GCP_DEBUGMODE = args.debug
if GCP_DEBUGMODE:
    print 'GCP_LIST in debugmode is not usable by ODM.'

#quit()

# ---Configure---
# input Kordinaten File
COORDSTXT = 'koords.txt'
# output GCP_LIST_FILE
GCP_LIST_FILE = 'gcp_list.txt'
# Template Directory
IMAGE_TEMPLATE_DIR = 'gcp-templates'
# Image Directory
IMAGE_DIR = 'images'
# Image file extensions filter
ext_list = ['PNG','png','JPG','jpg','JPEG','jpeg','TIF','tif'];
# valid GCP heafer 
UTM_list = ['WGS84','wgs84']; #unused

# configure ant init search algorithm
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)


# ---~Configure---



# create image file list
imagePathList=[]
for file in glob.glob(IMAGE_DIR + '/*.*'):
  if file.rsplit('.',1)[1] in ext_list :
      imagePathList.append(file)
      

      
print "Found %d Images" % (len(imagePathList))


# open template Images
tmpImagePathList=[]
templateImg=[]
for file in glob.glob(IMAGE_TEMPLATE_DIR + '/*.*'):
  if file.rsplit('.',1)[1] in ext_list :
      print file
      tmpImagePathList.append(file)

tmpImagePathList.sort()
print "---sorted tmpImagePathList"
for row in tmpImagePathList:
    print row
    templateImg.append(cv2.imread(row,0))

      
print "Found %d Images-Templates" % (len(templateImg))

#quit()

# Init SIFT detector
sift = cv2.SIFT()

templateKp=[]
templateDes=[] 

# Find template images keypoints and discriptor with sift
print "Search keypoints in Template Images"
for i in range(len(templateImg)):
    tmpKp, tempDes = sift.detectAndCompute(templateImg[i],None)
    print "Found %d Keypoints in Template Image Nr. %d" % (len(tmpKp),i)
    templateKp.append(tmpKp)
    templateDes.append(tempDes)

    
# ---Processing---

AllImageResults=[]
for i in range(len(imagePathList)):
    
    imageInfo=[]
    imageInfo.append(imagePathList[i].rsplit('/',1)[1])
    print "Searching for Keypoints in Image %s" %(imagePathList[i])
    image = cv2.imread(imagePathList[i],0)
    imageKp, imageDes = sift.detectAndCompute(image,None)
    print "Found %d Keypoints in Image Nr. %s" % (len(imageKp),imagePathList[i])
    
    for u in range(len(templateKp)):
        
        matches = flann.knnMatch(templateDes[u],imageDes,k=2)
        
        
        # store all the good matches as per Lowe's ratio test.
        good = []
        for m,n in matches:
            if m.distance < 0.7*n.distance:
                good.append(m)
        
        
        centroidXY = [0,0]
        
        paircord=[]
        paircord.append("P%d%s" % (u+1,":"))
        localTamplateKp = templateKp[u]
        if len(good)>MIN_MATCH_COUNT:
            src_pts = np.float32([ localTamplateKp[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
            dst_pts = np.float32([ imageKp[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
            matchesMask = mask.ravel().tolist()

            h,w = templateImg[u].shape
            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            dst = cv2.perspectiveTransform(pts,M)
                
            #print len(good)
            #print dst
            #print dst.shape
            #print dst[0,0,0]
            #print dst[2,0,0]
                
            # we calculate only for rectangle templates.
            # x center = (x0 - x2)/2 + x0
            # y center = (y0 - y1)/2 + y0
                
            if dst[0,0,0] == dst[2,0,0]:
                centroidXY[0] = dst[0,0,0]
                    
            if dst[0,0,0] < dst[2,0,0]:
                centroidXY[0] = (abs(dst[0,0,0] - dst[2,0,0]))/2 + dst[0,0,0]
            else:
                centroidXY[0] = (abs(dst[0,0,0] - dst[2,0,0]))/2 + dst[2,0,0]
                    

            if dst[0,0,1] == dst[2,0,1]:
                centroidXY[1] = dst[0,0,1]
                    
            if dst[0,0,1] < dst[2,0,1]:
                centroidXY[1] = (abs(dst[0,0,1] - dst[2,0,1]))/2 + dst[0,0,1]
            else:
                centroidXY[1] = (abs(dst[0,0,1] - dst[2,0,1]))/2 + dst[2,0,1]
                
            print "HIT, X=%d Y=%d" %(centroidXY[0],centroidXY[1])
            paircord.append("%d %d"%(centroidXY[0],centroidXY[1]))
                    
        else:
            print "FAIL, Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT) 
            paircord.append("F")
            
        
        imageInfo.append(paircord)
        print "Find %d matches between P%d and Image %d" %(len(good),u+1,i)
        
    AllImageResults.append(imageInfo)



AllImageResults.sort()


# create the gcp_txt file
infile = open(COORDSTXT, 'r')
outfile = open(GCP_LIST_FILE, 'w')


# example line
# 544256.7 5320919.9 5 3044 2622 IMG_0525.jpg

sortbyPmatches=[]

print "--------------Results--------------"
for i in range(len(AllImageResults)):
    print "------------Image--------------"
    print AllImageResults[i]
  
  
for i in range(len(templateImg)):
    searchstring = "P%d%s" % (i+1,":")
    for p in range(len(AllImageResults)):
        imageTempNameGetter = AllImageResults[p]
        imagename = imageTempNameGetter[0]
        for k in range(len(imageTempNameGetter)):
            if k>0:
                pointFinder = imageTempNameGetter[k]
                if pointFinder[0] == searchstring and pointFinder[1] !='F':
                    hitstring = (pointFinder[0] + " " + pointFinder[1] + " " + imagename)
                    sortbyPmatches.append(hitstring)
                    
            
print "sort by gcp_points"
#print sortbyPmatches
for row in sortbyPmatches:
    print row

# - end create gcp list file
myLineList=[]

for line in infile:
    line = line.replace('\n', '')
    myLineList.append(line)


#print len(myLineList)
#print myLineList
#for row in myLineList:
#    print row

# merge strings and write to file
mergedStrings=[]
for row in sortbyPmatches:
    
    internalresultsSplit = row.split(': ')
    internalresultsSplit.append("end")
    internalresultsPosNr = internalresultsSplit[0]
    internalresultsPosCoords = internalresultsSplit[1]
    
    
    for row in myLineList:
        koordsTextSlit = row.split(': ')
        koordsTextSlit.append("end")
        koordsTextPosNr = koordsTextSlit[0]
        koordsTextPosCoords = koordsTextSlit[1]
        # print "compare koordsTextPosNr: %s, against internalresultsPosNr: %s" %(koordsTextPosNr, internalresultsPosNr)
        if koordsTextPosNr == internalresultsPosNr:
            print "--good--"
            print koordsTextPosNr
            print internalresultsPosNr
            if GCP_DEBUGMODE:
                print "debugstring"
                debugstring = "%s %s %s" % (internalresultsPosNr, koordsTextPosCoords, internalresultsPosCoords)
                print debugstring
                mergedStrings.append(debugstring)
            else:
                print "normal string"
                normalstring = "%s %s" % (koordsTextPosCoords, internalresultsPosCoords)
                mergedStrings.append(normalstring)
                


# save first line
if GCP_DEBUGMODE:
    outfile.write("This file is only for debugging and contains P1 - Pn to find errors\n")
    
outfile.write(myLineList[0]+'\n')
for row in mergedStrings:
    outfile.write(row+'\n')

print "gcp_list.txt sorted by GCP"
for row in mergedStrings:
    print row


infile.close()
outfile.close()

print "--------"
print "finished gcp_list.txt"


# ---~Main---