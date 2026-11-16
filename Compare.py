from math import sqrt

from PIL import Image

img1 = Image.open('Blender.png')
img2 = Image.open('test.png')

errorList = []

for y in range(img1.width):
    for x in range(img1.height):
        p1 = img1.getpixel((x,y))
        p2 = img2.getpixel((x,y))
        errorList.append(sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]-p2[2])**2))

print(sum(errorList)/len(errorList))