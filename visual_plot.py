
#Importing libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os , shutil
from moviepy.editor import ImageClip ,concatenate_videoclips 
from tqdm import tqdm
import random 
from PIL import Image
import subprocess , shlex


def removeBackground(file_list): 
    print("\n>>> Removal of the white background")
    for file in tqdm(range(1,1+len(file_list))) : 
        blank_img = Image.new('RGBA',(800,500),(0,0,0))
        img = Image.open(file_list[file-1]) 
        img = img.convert("RGBA") 
        datas = img.getdata() 
        newData = []
        for item in datas : 
            if item[0] == 255 and item[1] == 255 and item[2] == 255 : 
                newData.append((255,255,255,0)) 
            else : 
                newData.append(item) 
        img.putdata(newData)
        w,h = blank_img.size
        blank_img.paste(img,(150,0))
        blank_img.save(file_list[file-1],"PNG")
        
def main(fileName) : 
    path = "Image_sort/"+str(fileName)+"/matplotlib" 
    os.makedirs(path)
    
    df = pd.read_excel("Image_sort/"+str(fileName)+"/frequency.xlsx")
    data = df.loc[:,"Frequency"] 
    lst = [] 
    for point in range(len(data)) : 
         lst.append(data[point]) 
    
    arr = np.asarray(lst) 
    update , points = [] , []
    file_list = []
    fps = 100    
    fig , ax = plt.subplots() 
        
    for plot in range(len(arr)) : 
        points.append(plot)
        update.append(arr[plot]) 
        
    part1 , part2 , part3 = round(len(points)/3) , (round(len(points)/3))*2  , len(points) 
    print("\n>>> Storing plot-wise frequencies range")
    for count in tqdm(range(len(points))) : 
        if count == 0 : 
            show_points = points[0],
            show_update = update[0],
            show_points , show_update = list(show_points) , list(show_update)
        if count != 0 :     
            if count < part1  : 
                index1 = random.randint(1,round(part1/3))
                index2 = random.randint(part1-10,part1)
        
            if count >= part1 and count<part3 : 
                index1 = random.randint(part1,part2)
                index2 = random.randint(part2,part3)
            show_points , show_update = points[index1:index2] , update[index1:index2]
            
        show_points = [4*i for i in show_points]   
        ax.clear()
        ax = plt.subplot(111, polar=True)
        fig.tight_layout()
        ax.axis("off")
        N = len(show_points)
        bottom = 5
        max_height = 4
        if N != 0 : 
            theta = np.linspace(0,2*np.pi,N,endpoint = False)
            radii = max_height*np.asarray(show_update)
            width = (2*np.pi) / (N)
            ax.bar(theta, radii, width=width, bottom=bottom,color="white",edgecolor = "black")      
                
        file= "Image_sort/"+str(fileName)+"/matplotlib/"+str(count+1)+".png"
        fig.savefig(file,bbox_inches='tight',pad_inches=0) 
        file_list.append(file) 
    
    removeBackground(file_list)
    
    clips = [ImageClip(m).set_duration(1)
         for m in file_list]

    concat_clip = concatenate_videoclips(clips, method="compose")
    sped_up_video = concat_clip.speedx(factor=5.0)
    sped_up_video.write_videofile("Image_sort/"+str(fileName)+"/plot_freq.mp4", fps=fps)
    shutil.rmtree(path)
   
    #To overlay a video on another video by making black pixels all transparent in the overlaying video:  
    print("\nFormation of the final imgbg_output.mp4 and vidbg_output.mp4")
    cmd1 = '''ffmpeg -i Image_sort/'''+str(fileName)+'''/img_audio.mp4 -i Image_sort/'''+str(fileName)+'''/plot_freq.mp4 -filter_complex "[1]split[m][a]; [a]geq='if(gt(lum(X,Y),51),255,0)', hue=s=0[al]; [m][al]alphamerge[ovr]; [0][ovr]overlay" Image_sort/'''+str(fileName)+'''/imgbg_output.mp4'''
    subprocess.call(shlex.split(cmd1))
    
    cmd2 = '''ffmpeg -i Image_sort/'''+str(fileName)+'''/video_audio.mp4 -i Image_sort/'''+str(fileName)+'''/plot_freq.mp4 -filter_complex "[1]split[m][a]; [a]geq='if(gt(lum(X,Y),51),255,0)', hue=s=0[al]; [m][al]alphamerge[ovr]; [0][ovr]overlay" Image_sort/'''+str(fileName)+'''/vidbg_output.mp4'''
    subprocess.call(shlex.split(cmd2))
    
    #Removing all the unnecessary files from the folder
    print("\nRemoving the unncessary files") 
    os.remove("Image_sort/"+str(fileName)+"/img_audio.mp4")
    os.remove("Image_sort/"+str(fileName)+"/video_audio.mp4")
    os.remove("Image_sort/"+str(fileName)+"/plot_freq.mp4")
    os.remove("Image_sort/"+str(fileName)+"/audio.wav")
    os.remove("Image_sort/"+str(fileName)+"/frequency.xlsx")
    os.remove("Image_sort/"+str(fileName)+"/output.xlsx")
    
    print("\nAll your files are saved in your folder "+str(fileName).capitalize())
    

    
    

    

    