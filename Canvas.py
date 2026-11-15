from MathClasses import Vec3
from PIL import Image

class Canvas:
    def __init__(self,resX:int,resY:int):
        self.resX = resX
        self.resY = resY

        self.pixelList:list[list[Vec3]]
        self.initialize()

        self.img = Image.new('RGB',(self.resX,self.resY))
    
    def __repr__(self):
        return '\n'.join([' '.join([col.toTupleRounded(2) for col in row]) for row in self.pixelList])

    def initialize(self):
        self.pixelList = []
        for _ in range(self.resY):
            self.pixelList.append([])
            for _ in range(self.resX):
                self.pixelList[-1].append(Vec3.ZERO)
    
    def putPixel(self,pos:tuple[int,int],color:Vec3):
        color.x = min(max(color.x,0),1)
        color.y = min(max(color.y,0),1)
        color.z = min(max(color.z,0),1)

        self.pixelList[pos[1]][pos[0]] = color

    def convertToImage(self):
        for y in range(self.resY):
            for x in range(self.resX):
                self.img.putpixel((x,y),(self.pixelList[y][x]*255).toIntTuple())
    
    def saveToFile(self,path:str):
        self.convertToImage()
        self.img.save(path,compress_level=0)