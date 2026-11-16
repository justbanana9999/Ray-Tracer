from MathClasses import Vec3
from Canvas import Canvas
from Shapes import Ray, Scene, Sphere
from intersections import raySphereIntersection, rayTriangleIntersection

class Camera:
    def __init__(self,pos:Vec3,pointAt:Vec3,res:tuple[int,int],focalLength:float,scene:Scene,maxBounces:int):
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

        self.scene = scene
        self.maxBounces = maxBounces
    
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

        bounce = 0
        while bounce < self.maxBounces+3:
            if bounce == self.maxBounces+2:
                return Vec3.ZERO
            hitList:list[tuple[Vec3,Vec3]] = []
            hit = False
            for shape in self.scene.shapeList:
                if isinstance(shape,Sphere):
                    hit,hitPos,hitNormal = raySphereIntersection(pixelRay,shape)
                # elif isinstance(shape,Triangle):
                else:
                    hit,hitPos,hitNormal = rayTriangleIntersection(pixelRay,shape)
                
                if hit:
                    hitList.append((hitPos,hitNormal))
            
            if len(hitList) == 0:
                # print(bounce,pixelRay)
                break
            else:
                hitList = sorted(hitList,key=lambda x: (pixelRay.origin-x[0]).length())
                # if bounce == 1:
                #     return Vec3.UP if len(hitList) == 1 else Vec3.RIGHT
                hitPos,hitNormal = hitList[0]
                pixelRay.vector = Vec3.reflect(pixelRay.vector,hitNormal)
                pixelRay.origin = hitPos
                # pixelRay.origin += pixelRay.vector*0.01
                # print(hitList)
                # print(bounce,pixelRay)
            bounce += 1
        
        return -pixelRay.vector
    
    def render(self):
        self.updateAxes()
        self.updateSizeAndCanvas()
        
        for y in range(self.res[1]):
            
            if y == 0 or y+1 == self.res[1] or y%100 == 0:
                print(f'\r{round((y+1)/self.res[1]*100,1)}%',end='',flush=True)

            for x in range(self.res[0]):
                color = self.shootRayFromPixel(x,y)
                self.canvas.putPixel((x,y),color)
        
        # print(self.canvas)
        self.canvas.saveToFile('test.png')

        print()