from MathClasses import Vec3

class Camera:
    def __init__(self,pos:Vec3,lookAt:Vec3,res:tuple[int,int],focalLength:float):
        self.res = res
        self.pos:Vec3 = pos
        self.lookAt:Vec3 = lookAt

        self.up:Vec3
        self.front:Vec3
        self.right:Vec3

        self.updateAxes()

        self.width:float
        self.height:float
    
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

    def getTopLeftPixel(self):
        self.width = min(self.res[0]/self.res[1],1)
        self.height = min(self.res[1]/self.res[0],1)


        self.topLeftPixel = -self.right*self.width/2 + self.up*self.height/2