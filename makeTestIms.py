'''
Python script to generate and save test images. Three images are created each
256x256 pixels and are named testIm1.png, testIm2.png and testIm3.png
respectively. Images are saved in the directory where this script is saved. The
first image has all pixels set to 128. The second runs from 0-256 incrementing
by eight after eight columns; rows have constant values. testIm3.png does the
same as 2 but has constant columns with rows running through those values.
'''

#import the Image module from PIL, it allows us to play with pictures
from PIL import Image

#the lists will hold the image data before we put it into the Image objects
imList1 = list()
imList2 = list()
imList3 = list()

#initialize variables I will use to generate image data
val1 = 128
val2 = 0
val3 = 0

#loop over the numbers 0, 1, 2, 3...65534, 65535 (256*256=65536)
for i in range(65536):
    #add a new element to the first list containing val1 for each iteration
    imList1.append(val1)
    #check if we are past the first row and if the current iteration is a
    #multiple of 2048 (8*256)
    if i > 255 and i % 2048 == 0:
        #equivalent to val2 = val2 + 8
        val2 += 8
    #append a new element to the second list containing val2
    imList2.append(val2)
    #check if the current iteration is a multiple of 256 (number of columns)
    #this resets val3 to zero for each row
    if i % 256 == 0:
        val3 = 0
    #check if the current iteration is a multiple of 8
    #this makes the pixel value increment by 8 after 8 columns
    if i % 8 == 0:
        #equivalent to val3 = val3 + 8
        val3 += 8
    #append a new element to the third list containing val3
    imList3.append(val3)

#create a new image called im1, mode set to 'L' (luminance?) and 256x256 pixels
im1 = Image.new('L', [256, 256])
#store the list of values I created in the for loop in this Image object
im1.putdata(imList1)
#uncomment this next line to immediately view image 1 upon executing this
#script
#im1.show()
#save im1 to the file testImage1.png in the same directory as this file is saved
im1.save('testImage1.png')
im2 = Image.new('L', [256, 256])
im2.putdata(imList2)
#im2.show()
im2.save('testImage2.png')
im3 = Image.new('L', [256, 256])
im3.putdata(imList3)
#im3.show()
im3.save('testImage3.png')
