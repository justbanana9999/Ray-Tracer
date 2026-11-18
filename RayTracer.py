from random import seed
from time import perf_counter

from MathClasses import Vec3
from Canvas import Canvas
from Shapes import Ray, Scene, Sphere, Material
from intersections import raySphereIntersection, rayTriangleIntersection

class Camera:
    def __init__(self,pos:Vec3,pointAt:Vec3,res:tuple[int,int],focalLength:float,scene:Scene,maxBounces:int,samples:int):
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
        self.samples = samples
    
    def updateAspectRatio(self):
        self.aspectRatio = self.res[0]/self.res[1]

    def updateAxes(self):
        self.front,self.right,self.up = Vec3.getRelativeAxes((self.lookAt-self.pos))
        
    def updateSizeAndCanvas(self):
        self.updateAspectRatio()
        self.width = min(self.aspectRatio,1)
        self.height = min(1/self.aspectRatio,1)

        self.canvas = Canvas(self.res[0],self.res[1])

    def getPixelLocalPos(self,x:int,y:int):

        self.pixelSize = self.width/self.res[0]

        self.topLeftPixel = -self.right*(self.width-self.pixelSize)/2 + self.up*(self.height-self.pixelSize)/2 + self.front*(self.focalLength/36)

        self.pixelPos = self.topLeftPixel + self.right*self.pixelSize*x - self.up*self.pixelSize*y
    
    def shootRayFromPixel(self,x:int,y:int) -> Vec3:
        colorList:list[Vec3] = []

        for _ in range(self.samples):
            self.getPixelLocalPos(x,y)
            pixelRay = Ray(self.pos,self.pixelPos.normalized())

            bounce = 0
            while bounce < self.maxBounces+3:
                if bounce == self.maxBounces+2:
                    pixelRay.color = Vec3.ZERO
                hitList:list[tuple[Vec3,Vec3,Material]] = []
                hit = False
                for shape in self.scene.shapeList:
                    if isinstance(shape,Sphere):
                        hit,hitPos,hitNormal = raySphereIntersection(pixelRay,shape)
                    # elif isinstance(shape,Triangle):
                    else:
                        hit,hitPos,hitNormal = rayTriangleIntersection(pixelRay,shape)
                    
                    if hit:
                        hitList.append((hitPos,hitNormal,shape.color))
                
                if len(hitList) == 0:
                    # print(bounce,pixelRay)
                    if bounce == 0:
                        pixelRay.color = Vec3.ZERO
                    break
                else:
                    hitList = sorted(hitList,key=lambda x: (pixelRay.origin-x[0]).length())
                    hitPos,hitNormal,hitColor = hitList[0]

                    diffuseVector = Vec3.scatterTowardsNormal(pixelRay.vector,hitNormal)
                    specularVector = Vec3.reflect(pixelRay.vector,hitNormal)
                    pixelRay.vector = Vec3.interpolate(specularVector,diffuseVector,hitColor.roughness**2).normalized()
                    
                    pixelRay.incoming += hitColor.emission * pixelRay.color
                    pixelRay.color *= hitColor.diffuse
                    
                    pixelRay.origin = hitPos

                    # pixelRay.origin += pixelRay.vector*0.01
                    
                bounce += 1
            
            # colorList.append(pixelRay.color)
            colorList.append(pixelRay.incoming)

        color = Vec3.average(colorList)

        # if (x,y) == (0,0):
        #     print(colorList)
        #     print(color)

        return color
    
    def render(self,progress:bool=False):
        tStart = perf_counter()
        tStart1 = perf_counter()
        tStart2 = tStart1
        self.updateAxes()
        self.updateSizeAndCanvas()
        
        rowSpeedAvg = 0
        rayCalcSpeedAvg = 0
        etaMeasureSize = 10
        renderedRows = -1
        
        for y in range(self.res[1]):
            
            renderedRows += 1
            if progress:
                # Updates progress every second.
                elapsed1 = perf_counter()-tStart1
                elapsed2 = perf_counter()-tStart2
                if elapsed2 > etaMeasureSize:
                    tStart2 = perf_counter()
                    rowSpeedAvg = renderedRows/etaMeasureSize
                    # pixels * samples
                    rayCalcSpeedAvg = int(rowSpeedAvg*self.res[0])
                    renderedRows = 0
                
                if elapsed1 > 0.5:
                    tStart1 = perf_counter()
                    percentage = f'{round((y+1)/self.res[1]*100,1)}%'
                    percentage = percentage.ljust(5,' ')

                    if rowSpeedAvg == 0:
                        if perf_counter()-tStart < 10:
                            eta = 'Gathering eta'
                        else:
                            eta = '∞'
                    else:
                        etaInt = int((self.res[1]-y)/rowSpeedAvg)
                        if etaInt >= 60:
                            eta = f'{etaInt//60} m {etaInt%60} s'
                        else:
                            eta = f'{etaInt} s'
                    end = ' '*10
                    print(f'\r{percentage} | {eta} | {rayCalcSpeedAvg} r/s {end}',end='',flush=True)

            for x in range(self.res[0]):
                seed(y*self.res[0]+x)
                color = self.shootRayFromPixel(x,y)
                self.canvas.putPixel((x,y),color)
        
        # print(self.canvas)
        self.canvas.saveToFile('test.png')

        if progress:
            print()
            # print(' '*50,end='\r')
        
        elapsed = round(perf_counter()-tStart,1)
        if elapsed >= 60:
            print(f'{int(elapsed//60)} m {int(elapsed%60)} s')
        else:
            print(f'{elapsed} s')
