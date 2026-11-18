from random import seed, shuffle
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

        return self.topLeftPixel + self.right*self.pixelSize*x - self.up*self.pixelSize*y
    
    def shootRayFromPixel(self,x:int,y:int) -> Vec3:
        colorList:list[Vec3] = []

        startPixelPos = self.getPixelLocalPos(x,y)

        triangleList:dict[str,(tuple[bool,Vec3,Vec3])] = {}

        for _ in range(self.samples):
            pixelRay = Ray(self.pos,startPixelPos.normalized())

            bounce = 0
            while bounce < self.maxBounces+3:
                if bounce == self.maxBounces+2:
                    pixelRay.color = Vec3.ZERO
                hitPos,hitNormal = Vec3.ZERO,Vec3.ZERO,
                closest = (Vec3.ZERO,Vec3.ZERO,Material())
                minDist = 1e6
                hit = False
                for shape in self.scene.shapeList:
                    if isinstance(shape,Sphere):
                        hit,hitPos,hitNormal = raySphereIntersection(pixelRay,shape)
                    else:
                        if bounce == 0:
                            if (s:=str(shape)) not in triangleList.keys():
                                triangleList[s] = rayTriangleIntersection(pixelRay,shape)
                            hit,hitPos,hitNormal = triangleList[s]
                        else:
                            hit,hitPos,hitNormal = rayTriangleIntersection(pixelRay,shape)
                    if hit:
                        if (d:=(hitPos-pixelRay.origin).length()) < minDist:
                            minDist = d
                            closest = (hitPos,hitNormal,shape.material)
                
                if minDist == 1e6:
                    if bounce == 0:
                        pixelRay.color = Vec3.ZERO
                    break
                else:
                    hitPos,hitNormal,hitColor = closest

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
    
    def render(self,progress:bool=False,etaMeasureSize:float=2):
        tStart = perf_counter()
        tStart1 = perf_counter()
        tStart2 = tStart1
        self.updateAxes()
        self.updateSizeAndCanvas()
        
        avgSpeed = 0
        renderedPixels = -1
        
        pixelIndex = -1

        remainingPixels:list[tuple[int,int]] = []

        for y in range(self.res[1]):
            for x in range(self.res[0]):
                remainingPixels.append((x,y))

        shuffle(remainingPixels)

        for x,y in remainingPixels:
            pixelIndex += 1
            renderedPixels += 1
            
            if progress:
                # Updates progress every second.
                elapsed1 = perf_counter()-tStart1
                elapsed2 = perf_counter()-tStart2
                
                if elapsed1 > 10:
                    tStart1 = perf_counter()
                    self.canvas.saveToFile('test.png')

                if elapsed2 > etaMeasureSize:
                    tStart2 = perf_counter()

                    percentage = f'{round((pixelIndex+1)/len(remainingPixels)*100,1)}%'
                    percentage = percentage.ljust(5,' ')

                    if avgSpeed == 0:
                        if perf_counter()-tStart < etaMeasureSize:
                            eta = 'Gathering eta'
                        else:
                            eta = 'infinity'
                    else:
                        etaInt = int((len(remainingPixels)-pixelIndex)/avgSpeed)
                        if etaInt >= 3600:
                            eta = f'{etaInt//3600} h {(etaInt%3600)//60} m {etaInt%60} s'
                        elif etaInt >= 60:
                            eta = f'{etaInt//60} m {etaInt%60} s'
                        else:
                            eta = f'{etaInt} s'
                    end = ' '*10
                    print(f'\r{percentage} | {eta} | {avgSpeed} px/s {end}',end='')
                    
                    avgSpeed = renderedPixels/etaMeasureSize
                    renderedPixels = 0

            seed(y*self.res[0]+x)
            color = self.shootRayFromPixel(x,y)
            self.canvas.putPixel((x,y),color)
        
        self.canvas.saveToFile('test.png')

        if progress:
            print('\r'+' '*50,end='')
        
        elapsed = round(perf_counter()-tStart,1)
        if elapsed >= 3600:
            print(f'\r{int(elapsed%3600)} h {int((elapsed%3600)//60)} m {int(elapsed%60)} s')
        elif elapsed >= 60:
            print(f'\r{int(elapsed//60)} m {int(elapsed%60)} s')
        else:
            print(f'\r{elapsed} s')
