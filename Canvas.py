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
        self.pixelList = [[Vec3.ZERO for _ in range(self.resX)] for _ in range(self.resY)]
    
    def putPixel(self,pos:tuple[int,int],color:Vec3):
        color.x = min(max(color.x,0),1)
        color.y = min(max(color.y,0),1)
        color.z = min(max(color.z,0),1)

        self.pixelList[pos[1]][pos[0]] = color

    def convertToImage(self):
        # print(self.pixelList[0][0])
        # print([pixel for pixel in [row for row in self.pixelList]])
        convertedList:list[tuple[int,int,int]] = []
        for row in self.pixelList:
            for pixel in row:
                convertedList.append(Vec3.toIntTuple(pixel*255))
        self.img.putdata(convertedList)  # pyright: ignore[reportUnknownMemberType]
        # for y in range(self.resY):
        #     for x in range(self.resX):
        #         self.img.putpixel((x,y),(self.pixelList[y][x]*255).toIntTuple())
    
    def saveToFile(self,path:str):
        self.convertToImage()
        self.img.save(path,compress_level=0)