import os, glob,shutil

files = glob.glob('/home/nate/Desktop/2018_4_2_07_30_02--2018_4_2_08_30_01/*.jpg')


files.sort()

for i in range(len(files)):
    os.rename(files[i], files[i][:-10]+'{:06d}.jpg'.format(i))
