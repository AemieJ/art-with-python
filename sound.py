#Importing libraries
import numpy as np 
import pandas as pd 
import math , colorsys
import librosa
from  more_itertools import unique_everseen
from scipy.io import wavfile
from tqdm import tqdm
import os , shutil 
import subprocess , shlex

#Importing external libraries from python file 
import visual_plot as plot

def main(fileName) : 
    PATH = "Image_sort/"+str(fileName)+"/wav"
    os.makedirs(PATH)
    df = pd.read_excel("Image_sort/"+str(fileName)+"/output.xlsx") 
    red = df.loc[:,"Red"] 
    green = df.loc[:,"Green"] 
    blue = df.loc[:,"Blue"] 
    sound =[] 
    print("\n>>> Calcuting sound frequency pixel-wise")
    for pixel in tqdm(range(1,1+len(df))) : 
         hue , sat , val = colorsys.rgb_to_hsv(red[pixel-1],green[pixel-1],blue[pixel-1]) 
         value = (hue*360) *(650-475) 
         wavelength = 650.0 - (value/240)
         frequency = 299792458/wavelength 
         frequency = frequency / 1000 
         sound_freq = round(10**(math.log(frequency,10)+12-12.04))
         sound.append(sound_freq)

    sound = list(unique_everseen(sound))
    df2 = pd.DataFrame(sound , columns=["Frequency"]) 
    df2.to_excel("Image_sort/"+str(fileName)+"/frequency.xlsx")

    sampleRate = 44100
    length = 2

    t = np.linspace(0, length, sampleRate * length)  #  Produces a 2 second Audio-File
    print("\n>>> Storing audio for pixel-wise frequency")
    for freq in tqdm(range(1,1+len(sound)))  :  
            y = np.sin(sound[freq-1] * 2 * np.pi * t)
            wavfile.write('Image_sort/'+str(fileName)+'/wav/audio'+str(freq)+'.wav', sampleRate,y)
            
    '''CONCATENATE ALL AUDIO FILES'''
    for freq in range(1) : 
        print("\n>>> Forming the audio file for the image")
        for freq_next in tqdm(range(1,len(sound))) : 
            _ , data1 = wavfile.read("Image_sort/"+str(fileName)+"/wav/audio"+str(freq+1)+".wav") 
            _ , data2 = wavfile.read("Image_sort/"+str(fileName)+"/wav/audio"+str(freq_next+1)+".wav")
            audio1 = np.hstack((data1,data2))
            wavfile.write("Image_sort/"+str(fileName)+"/wav/audio1.wav",sampleRate , audio1) 
            os.remove("Image_sort/"+str(fileName)+"/wav/audio"+str(freq_next+1)+".wav")

    #Fasten the speed of video without affecting its pitch
    shutil.move("Image_sort/"+str(fileName)+"/wav/audio1.wav","Image_sort/"+str(fileName)+"/audio1.wav") 
    shutil.rmtree("Image_sort/"+str(fileName)+"/wav")
    _ , data = wavfile.read("Image_sort/"+str(fileName)+"/audio1.wav") 
    data_fast = librosa.effects.time_stretch(data,10.0)
    wavfile.write("Image_sort/"+str(fileName)+"/audio.wav",sampleRate,data_fast) 
    os.remove("Image_sort/"+str(fileName)+"/audio1.wav")

    #To add music background to your image file , root down to your directory and execute : 
    print("\nCreation of img_audio and video_audio files")
    cmd1 = "ffmpeg -i Image_sort/"+str(fileName)+"/"+str(fileName)+".jpg -i Image_sort/"+str(fileName)+"/audio.wav -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest Image_sort/"+str(fileName)+"/img_audio.mp4"
    subprocess.call(shlex.split(cmd1)) 
    
    #To add music background to your video file  , root down to your directory and execute : 
    cmd2 = "ffmpeg -i Image_sort/"+str(fileName)+"/"+str(fileName)+".mp4 -i Image_sort/"+str(fileName)+"/audio.wav -filter_complex '[1:0] apad' -shortest Image_sort/"+str(fileName)+"/video_audio.mp4"
    subprocess.call(shlex.split(cmd2))
    
    plot.main(fileName)
    


