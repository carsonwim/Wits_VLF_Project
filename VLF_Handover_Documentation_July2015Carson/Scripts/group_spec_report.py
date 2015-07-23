#!/usr/bin/python2

# This Python Script has been taken/addapted from Fred Fourie (SANSA MARION ISLAND ENGINEER
# 2012-2013) original script called QGen.py. His script created a list in a file, which 
# was read into a function line by line to produce plots. I could not get this to work
# and had to resort to feeding command line arguments. :(. 
#
# This script basically creates high quality spectrograms from wav files, and compiles these 
# images into one consise PDF which can be reviewed by a SANSA MARION ISLAND ENGINEER in
# order to find annomalies in the VLF spectrum easily.

from scikits.audiolab import Sndfile
import numpy
import array
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime
import os
from PIL import Image
import reportlab
from reportlab.lib.pagesizes import letter, landscape ,A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak

listN = [] # list of file names


def plotSpectrogram(f,mode,channel):
    plt.close('all')
    # Extracting the name from the '.wav' file
    length = len(f)-1
    name = f[length-length :length-3]
    print "Processing: %s CH %s" % (name ,channel)
    plt.figure(figsize=(10.5,3), dpi=100); #figsize=(13,4)


    try:
# Some sound information
#	print "Input to Sndfile FN is %s" %f
        r = Sndfile(f)
        begin = 0 * r.samplerate
        stop = 59.8 * r.samplerate
        sample=r.read_frames(stop-begin)
# Setting out of some spectrogram variables
        Fs =  r.samplerate  #10000  
        NFFT = int(Fs*0.05) #*0.005)  # 5ms window
        noverlap = int(Fs*0.0025)
# Plotting
        fig= plt.specgram(sample[:,channel],Fs=Fs, NFFT=NFFT,noverlap=noverlap,
                         cmap=plt.get_cmap('jet'))
    except:
        print "Could not process %s" % name
        plt.figtext(0.5,0.5,"ERROR")
# Colourmap values that work well are: 'binary','bone' and 'jet'
  

    # plt.title(name)
    plt.title("CH"+str(channel)+" : "+f)
    plt.xticks([],[])  #gets rid of the x ticks and numbers
    plt.yticks([],[])  #gets rid of the y ticks and numbers

   
            # For normal plotting
            #    plt.title(f)
               
            #    plt.xlabel("Time (s)")
            #    plt.yticks([2000,4000,6000,8000,10000],[2,4,6,8,10])
            #    plt.ylabel("Frequency (kHz)")
                #plt.colorbar()
    try:
        # plt.savefig("./"+ name + ".png",fig=fig, bbox_inches='tight')
        plt.savefig(name+"CH"+str(channel)+".png",fig=fig, bbox_inches='tight')  #Save the results
        # if spectrogram has been sucessfully generated add it to the list of images that has$
        namePNG = "./" + name+"CH"+str(channel) + ".png"
        listN.append(namePNG)
#        print "Done."
    except:
        print "ERROR: %s" % name


def main():      
    arg = sys.argv
    count = 0
    mode = "d"
    
    for i in range(len(arg)):
    # Set the operation mode from arguments
        if i !=0:   # Ignore the first argument
            if arg[i][len(arg[i])-4:] == ".wav":
#		print "The input fine name is :"
              	print arg[i]
                plotSpectrogram(arg[i],mode,0)
                plotSpectrogram(arg[i],mode,1)
            else:
                print "Error: Unexcepted argument '%s' recieved." % arg[i]
                print "This script recieves .wav files and arguments as listed: \n-s (save plot only), \n-d (dislpay plot only) \n-sd (display and save plot)."
                sys.exit(1)

# Extracting the name from the '.wav' file
    tempname = arg[2]
    length = len(tempname)-1
    name = tempname[length-length :length-15]


# Open and setup a pdf
    pdfTitle = '%s-GROUP.pdf' % name 

    doc = SimpleDocTemplate(pdfTitle,pagesize=A4,
                            rightMargin=36,leftMargin=36,
                            topMargin=36,bottomMargin=9)
    c = canvas.Canvas(pdfTitle, pagesize=landscape(A4))

# Loop to fill pages with created spectrograms
    print "Compiling PDF..."
    count = 0
    listLen=len(listN)-1
    print listLen
    for i in range((listLen/2)+1):#(144):#(32):
        c.drawInlineImage(listN[count], 0*cm, 10*cm)
        print listN[count]
        if count+1 < len(listN) and count+2 <= len(listN):
                c.drawInlineImage(listN[count+1], 0*cm, 0*cm)
                print listN[count+1]
                count = count + 2
        c.showPage()

# Save the pdf and clean up
    c.save()
    print count
    os.system('rm ./*.png')
    print 'Done.'



                    
main()
