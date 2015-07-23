#!/usr/bin/python2

# This script recieves a mode argument and DVRAS .wav files to produce spectrograms.
# These plots can either be saved or displayed or both.
# For example: ./Spectrogram.py -d file.wav -s file.wav -sd file.wav
# These modes are:
#   -d  :   diplay plot
#   -s  :   save plot
#   -sd :   save and display plot (does also reciece '-ds')
# If no mode argument is set the default mode will be "display"
#
# Author:   Fred Fourie, 2012

from scikits.audiolab import Sndfile
import numpy
import array
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


#***************************************************************************************************
#***************************************************************************************************
def plotSpectrogram(f,mode,channel):
    print "Processing channel: %s" %channel
    plt.close('all')
# Extracting the name from the '.wav' file
    length = len(f)-1
    name = f[length-length :length-3]
    plt.figure(figsize=(13,4), dpi=100); #figsize=(13,4)

    try:
# Some sound information
	print "Input to Sndfile FN is %s" %f
        r = Sndfile(f)
        begin = 0 * r.samplerate
        stop = 59.8 * r.samplerate                          #This should be 60s.
        sample=r.read_frames(stop-begin)
# Setting out of some spectrogram variables
        Fs =  r.samplerate  #10000  
        NFFT = int(Fs*0.05) #*0.005)  # 5ms window
        noverlap = int(Fs*0.0025)
# Plotting
	# print "Sample is: %s" %sample
        fig= plt.specgram(sample[:,channel],Fs=Fs, NFFT=NFFT,noverlap=noverlap,
                         cmap=plt.get_cmap('jet'))
    except:
        print "Could not process %s" % name
        plt.figtext(0.5,0.5,"ERROR")
# Colourmap values that work well are: 'binary','bone' and 'jet'
  
# For compact mode
##    plt.title(f)
##    plt.xticks([],[])  #gets rid of the x ticks and numbers
##    plt.yticks([],[])  #gets rid of the y ticks and numbers

   
# For normal plotting
    plt.title("CH"+str(channel)+" : "+f)
   
    plt.xlabel("Time (s)")
    plt.yticks([2000,4000,6000,8000,10000],[2,4,6,8,10])
    plt.ylabel("Frequency (kHz)")
    plt.colorbar()

# Determine action based on mode argument
    if mode == 'd' or mode == 'sd':
        plt.show()
    if mode == 's' or mode == 'sd':
        plt.savefig(name+"CH"+str(channel)+".png",fig=fig, bbox_inches='tight')  #Save the results
    
    print "Done."

#***************************************************************************************************
#***************************************************************************************************
#***************************************************************************************************
def main():      
    arg = sys.argv
    count = 0
    mode = "d"
    
    for i in range(len(arg)):
    # Set the operation mode from arguments
        if i !=0:   # Ignore the first argument
            if arg[i] == '-d' or arg[i] == '-s' or arg[i] == '-sd' or arg[i] == '-ds' or arg[i][len(arg[i])-4:] == ".wav":
                if arg[i] == '-d':
                    mode = "d"
                if arg[i] == '-s':
                    mode = "s"
                if arg[i] == '-sd' or arg[i] == '-ds' :
                    mode = "sd"                   
                if arg[i][len(arg[i])-4:]== ".wav": 
		    print "The input fine name is :"
                    print arg[i]
                    plotSpectrogram(arg[i],mode,0)
                    plotSpectrogram(arg[i],mode,1)
            else:
                print "Error: Unexcepted argument '%s' recieved." % arg[i]
                print "This script recieves .wav files and arguments as listed: \n-s (save plot only), \n-d (dislpay plot only) \n-sd (display and save plot)."
                sys.exit(1)
                    
main()
