'''
This will house the image averaging function for now while we flesh it out. I
imagine this being absorbed into a more general image stacking function or
module where other stacking functions can live. Something like "StackIms" which
then could be imported and these function can be used like "StackIms.average()."
'''

#Try to import PIL in either of the two ways it can end up installed.
try:
    from PIL import Image
except ImportError:
    import Image
import os

def averageImages(imageList, upLCorner=0, outMode=None, outName='Average',
                  overWrite=False):
    """Averages together a list of images and saves the average to disk.

    Computes the average at each pixel of a list of images and constructs an
    average image which is saved to disk. Handles L and F mode images but can
    only save PNG output images.

    Parameters:
    imageList - List of strings specifying paths to images for averaging.
    upLCorner - List of 2-tuples specifying the coordinates of the upper left
                corner for each image if not all images are the same shape.
                Coordinates correspond to the location in the largest given
                image. Tuples go as (column index, row index) starting in the
                upper left corner of the image and are zero-based.
    outMode - String specifying the mode to save the average image as. Can be
              'L' or 'F'. If not specified, the output mode is set to the
              same as the first image in imageList.
    outName - String specifying the output image name. Defaults to "Average"
              with ".png" currently appended to the end since that is the only
              format that can be written.
    overWrite - Boolean specifying if the output image should overwrite a
                preexisting file with the same name or not.
    """
    #check if anything with the output name already exists
    if os.path.isfile(outName + '.png') and not overWrite:
        raise ValueError('A file already exists named ' + \
                         outName + '.png and overWrite=False.')

    #check more than 1 image is input
    if len(imageList) == 1:
        raise ValueError('Only a single image was input.')

    #check input images exist and are acceptable mode
    for imName in imageList:
        if not os.path.isfile(imName):
            raise ValueError("'" + imName + "' does not exist.")
        firstMode = Image.open(imName).mode
        if firstMode != 'L' and firstMode != 'F':
            raise IOError("'" + firstMode + "' mode not supported.")

    #check if the shapes of each image are the same
    maxShape = Image.open(imageList[0]).size
    sameShapes = True
    for imName in imageList:
        imObject = Image.open(imName)
        if imObject.size > maxShape:
            maxShape = imObject.size
            sameShapes = False
        elif imObject.size < maxShape:
            sameShapes = False

    #report images aren't all same shape and what we'll do about it
    if not sameShapes:
        print 'averageImages()::Not all images are the same shape.'
        if type(upLCorner) == int:
            print 'averageImages()::No coordinates given for image ' +\
                  'placement, will place all upper left corners at (0, 0) ' + \
                  'of largest image.'
        else:
            print 'averageImages()::Using specified upper left coordinates ' + \
                  'given:'

    #check if the modes of each image are the same
    firstMode = Image.open(imageList[0]).mode
    sameModes = True
    for imName in imageList:
        imObject = Image.open(imName)
        if imObject.mode != firstMode:
            sameModes = False

    #check if outMode is specified and define it if not, do some reporting too
    if outMode == None:
        outMode = firstMode
        if sameModes == False:
            print 'averageImages()::outMode not specified and given images ' + \
                  'are of different modes.'
            print 'averageImages()::Setting outMode to same mode as ' + \
                  'first image in imageList: ' + firstMode + '.'

    #loop over images building up set of average values
    avgVal = list()
    for i in range(len(imageList)):
        #images not same shape so zero-pad smaller ones and then average
        if not sameShapes:
             #no corner specified, defaulting to all (0, 0) upper left corners
            if type(upLCorner) == int:
                imObject = Image.open(imageList[i])
                junkIm = Image.new(imObject.mode, list(maxShape))
                junkIm.paste(imObject, (0, 0))
                imVal = junkIm.getdata()
            #instead, use specified corners
            else:
                imObject = Image.open(imageList[i])
                junkIm = Image.new(imObject.mode, list(maxShape))
                junkIm.paste(imObject, upLCorner[i])
                imVal = junkIm.getdata()
                print ' '*17 + imageList[i] + ': ' + str(upLCorner[i])
        #images are same shape so simply average images
        else:
            imObject = Image.open(imageList[i])
            imVal = imObject.getdata()
        #first image through has to fill out the average data list
        if len(avgVal) == 0:
            for i in range(len(imVal)):
                avgVal.append(imVal[i]/float(len(imageList)))
        #now just add to the pixel values
        else:
            for i in range(len(imVal)):
                avgVal[i] += imVal[i]/float(len(imageList))

    #cast average values into integers if outMode is L or I
    if outMode != 'F':
        for i in range(len(avgVal)):
            avgVal[i] = int(avgVal[i])

    #setup the average image and save to disk
    avgObject = Image.new(outMode, list(imObject.size))
    avgObject.putdata(avgVal)
    avgObject.save(outName + '.png')


#This is how we are currently testing this function. Simply running this file
#will execute the function allowing us to see if it's working as it should be.
averageImages(['C:\\Users\\Owner\\Desktop\\testImage2.png', \
               'C:\\Users\\Owner\\Desktop\\testImage1.png', \
               'C:\\Users\\Owner\\Desktop\\testImage3.png'])
#averageImages(['C:\\Users\\Nate\\Desktop\\new\\testImage2.png', \
#               'C:\\Users\\Nate\\Desktop\\new\\testImage1.png', \
#               'C:\\Users\\Nate\\Desktop\\new\\testImage3.tiff'], [(0, 0), \
#                                                                   (0, 25), \
#                                                                   (0, 0)], \
#              outMode='F')
