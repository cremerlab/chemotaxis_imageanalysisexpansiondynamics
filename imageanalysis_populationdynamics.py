###################################################################################
#Image analysis script to observe bacterial populations expanding in soft agar
###################################################################################
#Code to analyze raw confocal microscope images when observing chemotactic expansion
#and population growth of bacteria in soft-agar.
#
#The script works with the raw image and meta data export provided by the Leica
#Application Suite, Leica Microsystems (using option export as tif files (raw)).
#
#We used this code to analyze images acquired with a Leica Microsystems SP8 confocal
#microscope. Images were collected scanning samples in low-magnification, 
#tile-scanning along one axes (x) and through the agar (z).
#Additional details and the biological context are provided in our  manuscript:
#J.Cremer, T.Honda, Y.Tang, J. Wong-Ng, M.Vergassola, T.Hwa 
#"Chemotaxis as a navigation strategy to thrive in nutrient-replete environments"
#
#August 2019, Jonas Cremer and all coauthors.
###################################################################################
#required modules: numpy, scipy, PIL
#this script was tested and run with Python 2.7
###################################################################################

#read in required libraries
import sys
import os
import time
import csv
import numpy as np
import scipy
from scipy.ndimage import measurements

import PIL
from PIL import Image

###################################################################################
#main setting: set sub-folder name were images are stored
###################################################################################
filename = "glycerol20mM_100uasp100user_december2018" 

###################################################################################
#other settings
###################################################################################
thresholdv=20 #treshold intensity settings for treshold analysis.
rawdatafolder=os.path.join("/Volumes/Seagate Backup Plus Drive",filename)#set folder were raw-data is stored
mainfolder=os.path.join("/Users/jonascremer/Desktop/chemotaxis_writing/confocal/",filename) #set folder were results should be stored

#generate needed folders
try:
    os.makedirs(mainfolder)
except:
	pass
digestdatafolder=os.path.join(mainfolder,"digestdata")
try:
    os.makedirs(digestdatafolder)
except:
	pass
movieoutputfolder=os.path.join(mainfolder,"movieoutput")
try:
    os.makedirs(movieoutputfolder)
except:
	pass

###################################################################################
#start main code
###################################################################################

###################################################################################
#go through Folder and determine number of tile-scans, z-steps, and t-steps, and color-channels
###################################################################################
listfiles=os.listdir(rawdatafolder)
maxS=0 #tile scans
maxT=0 #time scans
maxC=0 #color channels
maxZ=0 #z-scans
numimg=0
for i in listfiles:
  if len(i.split("."))>1 and i.split(".")[-1]=="tif":
      numimg=numimg+1
      namestr=i.split(".")[-2].split("_")
      #this assumes the standard file output format from Leica SP8. 
      #format should be sth like xy_001_t0_s2_z79_ch00.tif
      #if different time-steps are not used, then output is simpler:
      #for example: Experiment_D1_s11_z078_ch00.tif
      Cc=int(namestr[-1][2:])
      Zc=int(namestr[-2][1:])
      print namestr
      try:
          Sc=int(namestr[-3][1:])
      except:
          Sc=0
      try:
          Tcc=int(namestr[-4][1:])
          Tclabel=namestr[-4][:1]
          if Tclabel=="t":
              Tc=Tcc
          else:
              
              Tc=-1
      except:
          Tc=-1

      if maxS<Sc:
          maxS=Sc
      if maxT<Tc:
          maxT=Tc
      if maxC<Cc:
          maxC=Cc
      if maxZ<Zc:
          maxZ=Zc

#correct length
maxC=maxC+1
maxZ=maxZ+1
maxS=maxS+1
maxT=maxT+1

#simple consistency check: are all images in folder covered?
if (numimg) != maxT*maxS*maxZ*maxC:
    print maxT
    print maxS
    print maxZ
    print "Wrong length"
    error
else:
	print "Check successfull: correct number of images in folder"

#give output of how many images have been detected.
print "Read in of file with dimenions: Z="+str(maxZ)+" T="+str(maxT)+" S="+str(maxS)+" C="+str(maxC)

###################################################################################
#read in metadata file
###################################################################################
#analyze metadata: Standard metadata output of Leica SP8 Software suite is a subfolder within the folder with the raw image data
metafolder=os.path.join(rawdatafolder,"MetaData")
listoutputmeta=os.listdir(metafolder)
for i in listoutputmeta: ##go through list and find file
  if len(i.split("_"))>1 and i.split("_")[-1]=="Properties.xml":
  	filenmacemeta=i
  	break
	
filenmacemeta=os.path.join(metafolder,filenmacemeta)
path_meta=os.path.join(digestdatafolder,"metadata.xml")
open(path_meta, "w").writelines([l for l in open(filenmacemeta).readlines() if 3>2])

###################################################################################
#go through all images
###################################################################################
#get name of experimet
for i in listfiles:
    if len(i.split("."))>1 and i.split(".")[-1]=="tif":
        if maxT>1:
            if len(i.split("_t"))>2:
                nameexpc=i.split("_t")[0]+"_t"+i.split("_t")[1]
            else:
                nameexpc=i.split("_t")[0]
        else:
            nameexpc=i.split("_s")[0]
        
for Tc in range(0,maxT):#go through every time step
    for Cc in range(0,maxC):#go through every color
        filestr="T"+str(Tc)+"_C"+str(Cc)
        intensitylist=[]
        print "processing "+filestr+" ..."
        for Sc in range(0,maxS):
            intensitylist.append([])
            #print "Sc: "+str(Sc)
            for Zc in range(0,maxZ):
          
                #first: get file name right
                if 3>2:
                    if maxT>10:
                        if Tc==0:
                            Tcstr="00"
                        elif Tc<10:
                            Tcstr="0"+str(Tc)
                        else:
                            Tcstr=str(Tc)
                    else:
                        Tcstr=str(Tc)
                    if Sc==0:
                        if maxS<11:
                            Scstr="0"
                        else:
                            Scstr="00"
                    elif Sc<10:
                        if maxS<11:
                            Scstr=""+str(Sc)
                        else:
                            Scstr="0"+str(Sc)
                    else:
                        Scstr=str(Sc)
                    if Zc==0:
                        Zcstr="00"
                    elif Zc<10:
                        Zcstr="0"+str(Zc)
                    else:
                        Zcstr=str(Zc)
                    if maxZ>100:
                        if Zc==0:
                            Zcstr="000"
                        elif Zc<10:
                            Zcstr="00"+str(Zc)
                        elif Zc<100:
                            Zcstr="0"+str(Zc)
                        else:
                            Zcstr=str(Zc)
                        
                        
                    #typical name, one timestep: Experiment001_3-03_s00_z01_ch00.tif
                    #typical name, several timesteps: Experiment001_TileScan_001_t28_s43_z90_ch00.tif
                    if maxT>100:
                        if Tc<100:
                            filenamecurrent=nameexpc+"_t0"+Tcstr+"_s"+Scstr+"_z"+Zcstr+"_ch0"+str(Cc)+".tif"
                        else:
                            filenamecurrent=nameexpc+"_t"+Tcstr+"_s"+Scstr+"_z"+Zcstr+"_ch0"+str(Cc)+".tif"
                    elif maxT>1:
                        filenamecurrent=nameexpc+"_t"+Tcstr+"_s"+Scstr+"_z"+Zcstr+"_ch0"+str(Cc)+".tif"
                    else:
                        filenamecurrent=nameexpc+"_s"+Scstr+"_z"+Zcstr+"_ch0"+str(Cc)+".tif"
                    
                    filenamcec=filenamecurrent
                #find correct file - go through list and find right properties
                else:
                 for i in listfiles:
                    if len(i.split("."))>1 and i.split(".")[-1]=="tif":
                        namestr=i.split(".")[-2].split("_")
                        if maxT<=1 and (Cc==int(namestr[-1][2:]) and Zc==int(namestr[-2][1:]) and Sc==int(namestr[-3][1:])):
                           filenamcec=i
                           break
                        elif (Cc==int(namestr[-1][2:]) and Zc==int(namestr[-2][1:]) and Sc==int(namestr[-3][1:]) and Tc==int(namestr[-4][1:])):
                            filenamcec=i
                            #print filenamcec
                            break
                
                #open image
                filenamec=os.path.join(rawdatafolder,filenamcec)
                try:
                    imarr=np.array(Image.open(filenamec),dtype=np.float)
                except:
                    print "unable to open..."
                    print filenamec
                    
                
                #start image analysis
                imarr[imarr < thresholdv] = 0
                intensitycurimg=np.mean(imarr)
        
                #generate binary image      
                imarrts=np.copy(imarr)
                imarrts[imarrts >= thresholdv] = 1
                #get clusters on image
                sbindiagnoal=scipy.ndimage.morphology.generate_binary_structure(2,2)
                #possible: add cluster analysis here
                
                #use from scipy.ndimage import measurements
                labeled_array, numberclusters_curimg = measurements.label(imarrts, structure=sbindiagnoal)
                areacurimg = measurements.sum(imarrts, labeled_array,index=np.arange(labeled_array.max() + 1))
                
                if np.nanmax(areacurimg)>40:
                    Imgtreshhold=1
                else:
                    Imgtreshhold=0
                
                areacurimg_avsize=np.mean(areacurimg)
                areacurimg_stdsize=np.std(areacurimg)
                
                #add different image information to list
                intensitylist[-1].append([np.mean(imarr),numberclusters_curimg,areacurimg_avsize,areacurimg_stdsize,Imgtreshhold])
                
                
        #save analysis output
        path_stat=os.path.join(digestdatafolder,filestr+"_stat.csv")
        f=open(path_stat, "wb")
        writer = csv.writer(f)
        writer.writerows(intensitylist)
        f.close()
   