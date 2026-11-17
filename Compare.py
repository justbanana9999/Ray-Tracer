from math import sqrt

from PIL import Image

img1 = Image.open('Blender.png')
img2 = Image.open('test copy.png')

errorList = []

for y in range(img1.width):
    for x in range(img1.height):
        p1 = img1.getpixel((x,y))
        p1 = (p1[0]/255,p1[1]/255,p1[2]/255)
        p2 = img2.getpixel((x,y))
        p2 = (p2[0]/255,p2[1]/255,p2[2]/255)
        errorList.append(sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]-p2[2])**2))

error = sum(errorList)/len(errorList)/sqrt(3)*100

print(f'Error: {round(error,2)} / 100')