from MathClasses import Vec3
from Canvas import Canvas

class Ray:
    def __init__(self,pos:Vec3,direction:Vec3):
        self.pos = pos
        self.direction = direction

class Camera:
    def __init__(self,pos:Vec3,pointAt:Vec3,res:tuple[int,int],focalLength:float):
        self.res = res
        self.pos = pos
        self.lookAt = pointAt
        self.focalLength = focalLength

        self.up:Vec3
        self.front:Vec3
        self.right:Vec3

        self.width:float
        self.height:float
        self.aspectRatio:float

        self.pixelSize:float
        self.pixelPos:Vec3

        self.canvas:Canvas
    
    def updateAspectRatio(self):
        self.aspectRatio = self.res[0]/self.res[1]

    def updateAxes(self):
        if self.pos == self.lookAt:
            self.front = Vec3(0,0,-1)
        else:
            self.front = (self.lookAt-self.pos).normalized()
        
        if self.front == Vec3.UP:
            self.right = Vec3(-1,0,0)
        elif self.front == -Vec3.UP:
            self.right = Vec3(1,0,0)
        else:
            self.right = Vec3.cross(self.front,Vec3.UP)
    
        self.up = Vec3.cross(self.right,self.front)

    def updateSizeAndCanvas(self):
        self.updateAspectRatio()
        self.width = min(self.aspectRatio,1)
        self.height = min(1/self.aspectRatio,1)

        self.canvas = Canvas(self.res[0],self.res[1])

    def getPixelWorldPos(self,x:int,y:int):

        self.pixelSize = self.width/self.res[0]

        self.topLeftPixel = -self.right*(self.width-self.pixelSize)/2 + self.up*(self.height-self.pixelSize)/2 + self.front*(self.focalLength/36)

        self.pixelPos = self.topLeftPixel + self.right*self.pixelSize*x - self.up*self.pixelSize*y
    
    def shootRayFromPixel(self,x:int,y:int) -> Vec3:
        self.getPixelWorldPos(x,y)
        pixelRay = Ray(self.pos,(self.pixelPos-self.pos).normalized())
        return pixelRay.direction
    
    def render(self):
        self.updateAxes()
        self.updateSizeAndCanvas()
        
        for y in range(self.res[1]):
            for x in range(self.res[0]):
                color = self.shootRayFromPixel(x,y)
                # if (x,y) == (49,0):
                #     print(color.toTupleRounded(1))
                # color.x = 1-(color.x+1)/2
                # color.y = 1-(color.y+1)/2
                # color.z = 1-(color.z+1)/2
                # color = Vec3.ONE-color
                # color = -color*2-Vec3.ONE
                color = -color
                self.canvas.putPixel((x,y),color)
        
        # print(self.canvas)
        self.canvas.saveToFile('test.png')