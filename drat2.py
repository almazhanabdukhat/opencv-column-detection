import cv2
import numpy as np
import pytesseract
import sys 
import numpy as np 
import os
import glob
import itertools

 
#can change the following line to point to the folder where tesseract is installed
pytesseract.pytesseract.tesseract_cmd = r"/usr/local/bin/tesseract"
def main():
    #short image example
    #putBoxes("1972.JPG")
    #images=read_images()
    
    input_folder="imgss/*.JPG"
    images = [cv2.imread(file) for file in glob.glob("imgss/*.JPG")]
    fnames = [glob.glob("imgss/*.JPG") for ext in "imgss/*.JPG"]
    fnames = list(itertools.chain.from_iterable(fnames))
    if images is None:
        print("images are null")
    else:
        print("images are not null")
        count=0

    names={}

    for img in images:
            filename=fnames[count]
            filename=filename.split("/")[len(filename.split("/"))-1]
            print("image name is " + filename)
            #filename = path.split("/")[len(path.split("/")-1]
            #filenames.append(filename)
            count=count+1
            print("image number" + str(count))
            height, width, channels = img.shape 
            dictLists={}
            print("height:"+str(height))
            img = cv2.resize(img, None, fx=0.48, fy=0.5)

            imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(imgray, 0, 255, cv2.THRESH_BINARY_INV)

            kernal = np.ones((5,5), np.uint8)
            #increase area of the object
            dilation = cv2.dilate(mask, kernal, iterations=7)
            #cv2.imshow("dilation",	dilation)
            ret,thresh = cv2.threshold(dilation,0, 255, 0)

            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            #print(len(contours))

            maximum=4
            for cnt in contours:
                #(x,y) be the top-left coordinate of the rectangle and (w,h) be its width and height.
                x,y,w,h = cv2.boundingRect(cnt)
                if maximum<h:
                    maximum=h
            print("maximum height: "+ str(maximum))
 
            count_lines=-1
            for cnt in contours:
                #(x,y) be the top-left coordinate of the rectangle and (w,h) be its width and height.
                x,y,w,h = cv2.boundingRect(cnt)
                if h+200>=maximum:
                    #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                    #print(y+h)
                    cv2.line(img, (x+w+5,y), (x+w+10,y+h), (122, 122, 122), 4)
                    cv2.line(img, (x+w+5,y), (x+w+10,y+h), (122, 122, 122), 4)
                    cv2.line(img, (x-5,y), (x-5,y+h), (122, 122, 122), 4)

                    count_lines+=1
            print("number of lines:" + str(count_lines))


            #color =	cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            img2 = cv2.drawContours(img, contours,	-1, (0,255,0),	2)
            #img2 = cv2.drawContours(dilation, contours,	-1, (122,122,255),	3)
            cv2.imshow("contours orig",	img2)
            result_folder="img_out/"
            cv2.imwrite(result_folder+filename, img2) # This is where there seems to be a problem
            #cv2.waitKey()
            #cv2.destroyAllWindows()

if __name__ == "__main__":
    main()  
