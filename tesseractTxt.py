'''
Author: Alma (Almazhan) Abdukhat
The program detects words in an image and puts boxes around the words based on the height, width of the bounding box,
x, y coordinates. Then the program separates words into lines based on the confidence levels, y-coordinates by creating dictionary of words
with similar y coordinates. Some symbols are blacklisted (non-alphanumerical) and text was detected with tesseract's image_to_data,
function. The program is a more evolved version of crowdOcr.py program and allows grouping by lines in contrast to tesseract's default
grouping of words into one column
'''

import cv2
import sys 
import pytesseract
import numpy as np 
import os
import glob
import itertools



#can change the following line to point to the folder where tesseract is installed
pytesseract.pytesseract.tesseract_cmd = r"/usr/local/bin/tesseract"

#checks if dictionary contains a y-coordinate group
def lineTrue(dict, val):
    for i in dict:
        if abs(i-val)<=16:
            return i
    
    return 0
#get names of the images (i.e. "012.JPG")
def getNames(files):
    names = [glob.glob(img_file) for img_file in files]
    names = list(itertools.chain.from_iterable(names))
    return names

def main():
    #read images from the folder
    images = [cv2.imread(file) for file in glob.glob("example/*.JPG")]
   
    #read JPG images from the target folder and get their names
    files_to_read = ["example/*.JPG"]
    image_names = getNames(files_to_read)

    if images is None:
        print("image folder is null")
    else:
        count=0 #optional - how many images are processed
        for img in images:
            count=count+1
            img_name=image_names[images.index(img)]
            img_name=(img_name.split("/"))[1] #get image file name without folder name
            print("image name: "+str(img_name)) #show name of the image file
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            text = pytesseract.image_to_string(img)
            img = cv2.resize(img, None, fx=0.3, fy=0.3)
            hImg, wImg,_ = img.shape
            boxes = pytesseract.image_to_data(img,config="""-c  tessedit_char_blacklist=*!?&6@\\"® tessedit_char_whitelist=0123456789.,abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMOPQRSTUVWXYZ  """)
            strOut=""
            dictLists={}

            for x, b in enumerate(boxes.splitlines()):  # count is in x
                if x != 0:
                    b = b.split() #box bounding
                    print(b) #print a box
                    if len(b) >= 10:
                        #coordinates are x,y and width and height of the bounding box
                        #if not b[2].isdigit():
                            #print("here" + str(b[2])+str(b[3])+str(b[4]))
                        block,lineNum,wordNum,x, y, w, h = int(b[2]),int(b[4]),int(b[5]),int(b[6]), int(b[7]), int(b[8]), int(b[9])
                        #if conf = -1, no word is detected
                        if b[10] == '-1':
                            strOut+="\n"
                        if (b[10] != '-1') and (len(b) == 12):
                            word=b[11]
                            #strOut+= "line number:" + b[4]+ "y coordinate:" + str(y)+ " word"+ word
                            #grouping words based on y - by horizontal lines 
                            ret=lineTrue(dictLists,y) #if there is already a line/y group
                            if (y in dictLists): 
                                dictLists[y].append(word) #add the word to that line
                            elif (y not in dictLists and ret!=0):
                                if block=='1':
                                    word="top"+word
                                dictLists[ret].append(word)
                            else:
                                dictLists[y] = [word] #otherwise create a new line group

                        # recognizing/putting boxes around every word 
                        cv2.rectangle(img, (x, y), (w + x, h + y), (0, 0, 255), 1)  # (0,0,255) - red color, thickness=1   
            
            #output the read info to txt files
            finalStr=""
            for i,s in dictLists.items():
                print(*s) 
                for m in s:
                    finalStr+=m+" "
                finalStr+="\n"
            out = os.path.join("example_out/", str(img_name)+".txt") 
            file1 = open(out,"w")
            file1.write(finalStr)
            file1.close()

            #show image
            cv2.imshow("edited", img)
            cv2.waitKey(10000) 
                        


if __name__ == "__main__":
    main()  
