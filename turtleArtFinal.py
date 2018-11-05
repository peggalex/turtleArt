import turtle, math, random, time

screen = turtle.Screen()
print(screen.screensize())
screen.bgcolor("blue")
rangeNumPetals = {'lower':5,'upper':10}
rangeWidthPetal = {'lower':6, 'upper':9} # pixel width of petals
flowerCell = {'x':((rangeWidthPetal['upper']/2)**2)*2,'y':((rangeWidthPetal['upper']/2)**2)*3}
rangeLengthStalk = {'lower':25,'upper':75}
strokeStalk = 4
height = turtle.window_height()
padding = 50
flowerColors = ['red','lightblue','orange','pink']
rangeGround = {'x': {'lower': -screen.screensize()[0]+padding,\
    'upper': screen.screensize()[0]-padding} ,'y': {'lower':  -screen.screensize()[1]+padding, 'upper': 0}}
rangeGroundFull = {'x': {'lower': -screen.screensize()[0], 'upper': screen.screensize()[0]},\
    'y': {'lower': -screen.screensize()[1], 'upper': 0}}
rangeSky = {'x': {'lower': -screen.screensize()[0]+padding, 'upper':  screen.screensize()[1]-padding},\
    'y': {'lower':  screen.screensize()[1]//2, 'upper':screen.screensize()[1]-padding}}
rangeMountainHeight = {'lower':50,'upper': screen.screensize()[1]//2}
rangeMountainLength = {'lower':200,'upper': 300}
exhaustedCellCoords = [] # make sure that cells that have flowers are not replaced

lenCloud = 200 # pixel length of a cloud
rangeNumBumps = {'lower':3,'upper':6} # number of bumps in a cloud
rangeRadiiBumps = {'lower':1,'upper':1.5} # coefficient for a radius (radii?)
assert(rangeNumBumps['lower']>=3)
sun = {'pos':{'x': 150, 'y': 150},'radius':50} 

def rotationMatrix(vector: 'tuple(x,y)', angle: 'degrees')->'rotated tuple':
    '''rotation matrix: transformation matrix ax = b for
    | cos(x) -sin(x)| |i|
    |               | | | = b
    | sin(x) cos(x) | |j|

    and [i,j] = vector
    rotates around origin
    '''
    angleR = math.radians(angle)

    #matricies where first level is the rows, second level is the columns
    #this is to make multiplication easier
    A = [[math.cos(angleR),-(math.sin(angleR))],[math.sin(angleR),math.cos(angleR)]]
    b = [None,None]
    x = vector
    assert(len(A)==len(b))
    assert(len(b) == len(x))
    assert(all(len(row)==len(x) for row in A))

    for _columnB in range(len(b)):
        scalarB = 0
        for _columnX in range(len(x)):
            scalarB += A[_columnB][_columnX]*x[_columnX]
        b[_columnB] = int(scalarB) if int(scalarB)+0.5>scalarB else int(scalarB)+1 #int(x) always rounds down
    return tuple(b)

def rotateAroundPoint(vector, point, angle)->'rotated tuple':
    if point == (0,0):
        return rotationMatrix(vector,angle)
    assert(len(vector)==len(point))
    vectorLessPoint = tuple(vector[i]-point[i] for i in range(len(vector)))
    vectorLessPointRotated = rotationMatrix(vectorLessPoint,angle)
    return tuple(vectorLessPointRotated[i]+point[i] for i in range(len(point)))

def getFlowerRadius(widthPetal: int, numPetals: "int pixels")->int:
    hypotenuse = widthPetal/2
    innerAngle = 360/numPetals
    return hypotenuse/(math.asin(math.radians(innerAngle/2)))

def getFlowerStartAngle(widthPetal: int, numPetals: int)->'angle degrees':
    def _getInteriorAngle(numPetals):
        return (180*(numPetals-2))/numPetals

    return -1*(180 - _getInteriorAngle(numPetals)/2 - 90)

class AnimatedObject:
    maxSerial = 0
    shapes = []
    # so there's no flash of a black default turtle
    # whenever a turt is initialised
    speed = 'fastest'

    # !! turtle is broken - 
    # calling clear() on a cloned turtle
    # doesn't work reliably with many points with pendown
    # as i learned spending an hour debugging !!

    def __init__(self):
        self.shapes = []
        self.polyColorDics = []

    def move(self):
        pass
    
    def getShapes():
        return self.shapes
    
    def clearDrawing(self):
        pass

    def getPolyColorDics(self):
        return self.polyColorDics

    def initTurt():
        cloud = turtle.Turtle()
        cloud.hideturtle()
        cloud.speed(AnimatedObject.speed)
        cloud.penup()
        return cloud
    
    def letThereBLight():
        turtle.register_shape("world",AnimatedObject.world)
        turt = turtle.Turtle("world")
        turt.seth(90)
        return turt

    def addShape(shape):
        #assume correct order
        # ie sun before clouds
        AnimatedObject.shapes.append(shape)

    def moveAll():
        for shape in AnimatedObject.shapes:
            shape.move()
            
    def clearDrawingAll():
        for shape in AnimatedObject.shapes:
            shape.clearDrawing()
    
    def getShape():
        world = turtle.Shape("compound")
        for shape in AnimatedObject.shapes:
            for polyColorDic in shape.getPolyColorDics():
                poly = polyColorDic['poly']
                color = polyColorDic['color']
                world.addcomponent(poly,color)
        turtle.register_shape("world",world)
        return "world"

class Ground(AnimatedObject):
    def __init__(self):
        super().__init__()
        AnimatedObject.addShape(self)
        self.ground = AnimatedObject.initTurt()
        self.genGround()

    def genGround(self)->None:
        ground = self.ground
        ground.pendown()
        ground.color("lightgreen")
        ground.begin_fill()
        ground.begin_poly()
        order = [('lower','upper'),('lower','lower'),('upper','lower'),('upper','upper')]
        for tup in order:
            ground.setpos(rangeGroundFull['x'][tup[0]],rangeGroundFull['y'][tup[1]])
        ground.end_fill()
        ground.end_poly()
        self.polyColorDics.append({'poly':ground.get_poly(),'color':"lightgreen"})
        ground.penup()

    def clearDrawing(self):
        self.ground.clear()
        
    
class Mountain(AnimatedObject):
    maxSerial = 0

    def __init__(self):
        super().__init__()
        AnimatedObject.addShape(self)
        self.mountain = AnimatedObject.initTurt()
        self.genMountain()

    def genMountain(self)->None:
        mountain = self.mountain
        mountain.penup()
        startingPosX = random.randint(rangeGround['x']['lower'],rangeGround['x']['upper'])
        startingPos = {'x':startingPosX,'y':0}
        mountainHeight = random.randint(rangeMountainHeight['lower'],rangeMountainHeight['upper'])
        mountainLength = random.randint(rangeMountainLength['lower'],rangeMountainLength['upper'])
        mountain.color("grey")
        mountain.setpos(startingPos['x']+(mountainLength/2),startingPos['y'])
        mountain.pendown()
        mountain.begin_poly()
        mountain.begin_fill()
        mountain.setpos(startingPos['x'],mountainHeight)
        mountain.setpos(startingPos['x']-(mountainLength/2),startingPos['y'])
        mountain.setpos(startingPos['x'],startingPos['y'])
        mountain.penup()
        mountain.end_fill()
        mountain.end_poly()
        self.polyColorDics.append({"poly":mountain.get_poly(),"color":"grey"})

    #@Override
    def clearDrawing(self):
        self.mountain.clear()


class Flower(AnimatedObject):
    maxSerial = 0
    amtToRotate = random.randint(1,3)
    
    def __init__(self):
        super().__init__()
        AnimatedObject.addShape(self)
        self.flower = AnimatedObject.initTurt()
        self.middle = AnimatedObject.initTurt()
        self.middle.color("yellow")
        self.middle.shape("circle")
        self.stalk = AnimatedObject.initTurt()
        stalk = self.stalk
        self.startingPetalPoly = None
        stalk.speed(self.speed)
        stalk.color("green")
        stalk.penup()
        self.angle = 0
        #stalk.pensize(3)
        self.startingPos = None
        self.genFlowers()
    
    def genFlowers(self)->None:
        def _genUniqueCoords(exhaustedCellCoords:'[int,]')->"{'x':int,'y':int}":
            while(True):
                    startingPosX = random.randint(rangeGround['x']['lower'],rangeGround['x']['upper'])
                    startingPosY = random.randint(rangeGround['y']['lower'],rangeGround['y']['upper'])
                    if ((startingPosX//flowerCell['x'],startingPosY//flowerCell['y']) not in exhaustedCellCoords):
                        exhaustedCellCoords.append((startingPosX//flowerCell['x'],startingPosY//flowerCell['y']))
                        return {'x':startingPosX,'y':startingPosY}
        def _drawStalk(startingPos: "{'x':int,'y':int}", widthPetal, numPetal):
            flowerRadius = getFlowerRadius(widthPetal, numPetals)
            lengthPetal = (widthPetal/2)**2
            stalk = self.stalk
            stalk.setpos(startingPos['x'],startingPos['y']-flowerRadius-(lengthPetal*2))
            stalk.pendown()
            stalk.begin_poly()
            stalk.setpos(startingPos['x'],startingPos['y'])
            stalk.penup()
            stalk.end_poly()
            self.polyColorDics.append({"poly":stalk.get_poly(),"color":"green"})

        def _drawPetals(startingPos,widthPetal, numPetals, colorPetal):
            flower = self.flower
            flower.penup()
            flower.hideturtle()
            flower.speed(self.speed)
            flowerRadius = getFlowerRadius(widthPetal, numPetals)
            vector = (startingPos['x']+flowerRadius,startingPos['y'])
            petalStartingPos = rotateAroundPoint(vector,(startingPos['x'],startingPos['y']),(180/numPetals)+90)
            flower.setpos(petalStartingPos[0],petalStartingPos[1])
            flower.setheading(90)
            flower.color(colorPetal)

            shape = [] #list o tuples
            firstPetal = [petalStartingPos]
            flower.pendown()
            flower.begin_fill()
            for i in range(int(-widthPetal/2), int(widthPetal/2)):
                pos = (flower.xcor()+1,flower.ycor()+(i**2)-((i+1)**2))
                flower.setpos(pos[0],pos[1])
                firstPetal.append(pos)
            shape.extend(firstPetal)

            for petal in range(1,numPetals):
                angle = -360*petal/numPetals
                for i in range(len(firstPetal)):
                    adjusted = rotateAroundPoint(firstPetal[i], (startingPos['x'],startingPos['y']),angle)
                    flower.setpos(adjusted)
                    shape.append(adjusted)
            shapeShifted = tuple((coord[0]-startingPos['x'],coord[1]-startingPos['y']) for coord in shape)
            flower.end_fill()
            flower.penup()
            self.polyColorDics.append({"poly":shape,"color":colorPetal})
            self.startingPetalPoly = shape
            
        def _drawMiddle(startingPos, widthPetal, numPetals):
            middle = self.middle
            middle.penup()
            flowerRadius = getFlowerRadius(widthPetal, numPetals)
            middle.setpos(startingPos['x'],startingPos['y']+flowerRadius)
            middle.setheading(180)
            middle.color("yellow")
            middle.begin_poly()
            middle.begin_fill()
            middle.circle(flowerRadius)
            middle.end_poly()
            middle.end_fill()
            self.polyColorDics.append({"poly":middle.get_poly(),"color":"yellow"})

            
        # main body of func
        self.startingPos = _genUniqueCoords(exhaustedCellCoords)
        numPetals = random.randint(rangeNumPetals['lower'],rangeNumPetals['upper'])
        widthPetal = random.randint(rangeWidthPetal['lower'],rangeWidthPetal['upper'])
        colorPetal = flowerColors[random.randint(0,len(flowerColors)-1)]

        _drawStalk(self.startingPos, widthPetal, numPetals)
        _drawPetals(self.startingPos, widthPetal, numPetals, colorPetal)
        _drawMiddle(self.startingPos, widthPetal, numPetals)
        

    #@Override
    def move(self):
        startingPosTup = (self.startingPos['x'],self.startingPos['y'])
        self.angle = self.angle%360
        self.angle -= self.amtToRotate
        for polyColorDic in self.polyColorDics:
            if polyColorDic['color'] == "yellow" or polyColorDic['color'] == "green":
                continue
            polyColorDic['poly'] = tuple(rotateAroundPoint(x,startingPosTup,self.angle) for x in self.startingPetalPoly)
            #self.angle-=self.amtToRotate
    #@Override
    def clearDrawing(self):
        self.stalk.clear()
        self.flower.clear()
        self.middle.clear()

class Cloud(AnimatedObject):
    maxSerial = 0
    amtToMove = 1 #pixels to the right
    
    def __init__(self):
        
        # when registering turtle shapes, the string name needs to be unique
        # do this by giving each cloud a unique tracking serial
        # increment global max to ensure unqiue values
        super().__init__()
        self.shape = None
        self.amtToMove = random.randint(1,3)
        AnimatedObject.addShape(self)
        self.cloud = AnimatedObject.initTurt()
        self.cloud.speed(self.speed)
        self.cloud.color("white")
        self.cloud.seth(-90)
        startingPosX = random.randint(rangeSky['x']['lower'],rangeSky['x']['upper'])
        startingPosY = random.randint(rangeSky['y']['lower'],rangeSky['y']['upper'])
        self.startingPos = {'x':startingPosX,'y':startingPosY}
        self.center = [startingPosX, startingPosY]
        self.numBumps = random.randint(rangeNumBumps['lower'],rangeNumBumps['upper'])
        self.bumps = {} # {int:{'length':int,'cummul':int,'radius':int'}, }
        bumps = self.bumps
        numBumps = self.numBumps
        self.genBumps()
        self.genCloud()

    def genBumps(self):
        numBumps = self.numBumps
        bumps = self.bumps
        for i in range(numBumps):
            bumps[i] = {}
            cloudsLeft = numBumps-i
            eBumpLength = lenCloud / cloudsLeft if i==0 else (lenCloud - bumps[i-1]['cummul']) / cloudsLeft
            # chance for bumpLength to be larger/smaller by a factor of 0.5
            lowerBound, upperBound = 0.5 * eBumpLength, 1.5 * eBumpLength
            bumpLength = random.randint(int(lowerBound),int(upperBound))
            assert(numBumps>=2)
            bumps[i]['length'] = bumpLength if i!=numBumps-1 else lenCloud - bumps[numBumps-2]['cummul']
            bumps[i]['cummul'] = bumpLength if i==0 else bumps[i-1]['cummul'] + bumpLength

            eRadius = int(bumps[i]['length'] / 2)
            bumps[i]['radius'] = eRadius if i==0 or i==numBumps-1 else random.randint(eRadius,eRadius*2)        

    def genCloud(self)->None:
        cloud = self.cloud
        cloud.penup()
        startingPos = self.startingPos
        bumps = self.bumps
        numBumps = self.numBumps
            # first bump:
        cloud.setpos(startingPos['x'],startingPos['y'])
        cloud.setheading(90)
                # length is a diameter so divide by 2, half circle so 180degrees
            # next bumps have random radius given length:
        for i in range(numBumps):
            cummul = 0 if i==0 else bumps[i-1]['cummul']
            center_xcor = startingPos['x']-int(bumps[i]['length']/2) - cummul
            cloud.setpos(center_xcor+bumps[i]['radius'],cloud.ycor())
            cloud.begin_poly()
            cloud.begin_fill()            # length is a diameter so divide by 2, half circle so 180degrees
            cloud.pendown()
            cloud.circle(bumps[i]['radius'],180,20)
            cloud.end_poly()
            cloud.end_fill()
            self.polyColorDics.append({"poly":cloud.get_poly(),"color":"white"})
            cloud.penup()
            cloud.setheading(90)

        cloud.setpos(startingPos['x'],startingPos['y'])
        self.cloud.seth(90)
        cloud.end_poly()
        cloud.end_fill()

    #@Override
    def clearDrawing(self):
        self.cloud.clear()
    
    #@Override
    def move(self):
        polys = self.polyColorDics
        shift = int(screen.screensize()[0]*2.5)
        if self.center[0]-lenCloud>screen.screensize()[0]:
            for poly in polys:
                poly['poly'] = tuple((x[0]-shift,x[1]) for x in poly['poly'])
            self.center[0] -= shift
        else:
            for poly in polys:
                poly['poly'] = tuple((x[0]+self.amtToMove,x[1]) for x in poly['poly'])
            self.center[0] += self.amtToMove


class Bird(AnimatedObject):
    radius = 20
    angle = 100
    size = 120
    inclineRange = 30 #degrees
    color = "grey"
    
    
    def __init__(self):
        
        # when registering turtle shapes, the string name needs to be unique
        # do this by giving each cloud a unique tracking serial
        # increment global max to ensure unqiue values
        super().__init__()
        self.shape = None
        AnimatedObject.addShape(self)
        self.bird = AnimatedObject.initTurt()
        self.bird.speed(self.speed)
        self.bird.color(Bird.color)
        self.amtToMove = random.randint(1,3)
        self.amtToRotate = random.randint(10,30)
        self.bird.penup()
        self.left = None
        self.right = None
        self.path = 0
        self.leftOriginalPoly = None
        self.rightOriginalPoly = None
        startingPosX = random.randint(rangeSky['x']['lower'],rangeSky['x']['upper'])
        startingPosY = random.randint(rangeSky['y']['lower'],rangeSky['y']['upper'])
        self.startingPos = {'x':startingPosX,'y':startingPosY}
        self.center = [startingPosX,startingPosY]
        self.genBird()

    def genBird(self)->None:
        turt = self.bird
        size = Bird.size
        radius = Bird.radius
        angle = Bird.angle
        startingPos = self.startingPos
        turt.setpos(startingPos['x'],startingPos['y'])
        turt.seth(size)
        turt.begin_poly()
        turt.pendown()
        turt.circle(radius,angle)
        turt.circle(radius,-angle)
        turt.end_poly()
        turt.penup()
        self.leftOriginalPoly = turt.get_poly()
        #self.leftOriginalPoly = tuple(rotateAroundPoint(x,self.center,90) for x in turt.get_poly())
        self.left = {"poly":self.leftOriginalPoly,"color":Bird.color}
        self.polyColorDics.append(self.left)

        turt.setpos(startingPos['x'],startingPos['y'])
        turt.seth(size*2)
        turt.begin_poly()
        turt.pendown()
        turt.circle(radius,-angle)
        turt.circle(radius,angle)
        turt.end_poly()
        turt.penup()
        #self.right = {"poly":turt.get_poly(),"color":"white"}
        #self.rightOriginalPoly = tuple(rotateAroundPoint(x,self.center,90) for x in turt.get_poly())
        self.rightOriginalPoly = turt.get_poly()
        self.right = {"poly":self.rightOriginalPoly,"color":Bird.color}
        self.polyColorDics.append(self.right)

    #@Override
    def clearDrawing(self):
        self.bird.clear()
    
    #@Override
    def move(self):

        polys = self.polyColorDics
        if self.center[0]+Bird.size<-screen.screensize()[0]:
            shift = int(screen.screensize()[0]*2.5)
            for poly in polys:
                poly['poly'] = tuple((x[0]+shift,x[1]) for x in poly['poly'])
            self.center[0] += shift
            self.leftOriginalPoly = tuple((x[0]+shift,x[1]) for x in self.leftOriginalPoly)
            self.rightOriginalPoly = tuple((x[0]+shift,x[1]) for x in self.rightOriginalPoly)
        else:
            for poly in polys:
                poly['poly'] = tuple((x[0]-self.amtToMove,x[1]) for x in poly['poly'])
            self.center[0] -= self.amtToMove
            self.leftOriginalPoly = tuple((x[0]-self.amtToMove,x[1]) for x in self.leftOriginalPoly)
            self.rightOriginalPoly = tuple((x[0]-self.amtToMove,x[1]) for x in self.rightOriginalPoly)
            
            incline = Bird.inclineRange * math.sin(math.radians(self.path))
            self.path += self.amtToRotate
            self.left['poly'] = tuple(rotateAroundPoint(x,self.center,incline) for x in self.leftOriginalPoly)
            self.right['poly'] = tuple(rotateAroundPoint(x,self.center,-incline) for x in self.rightOriginalPoly)
            
                


class Sun(AnimatedObject):
    amtToRotate = 1/2 #degrees
    suns = []
    def __init__(self):
        super().__init__()
        self.sun = AnimatedObject.initTurt()
        AnimatedObject.addShape(self)
        self.sun.speed('fastest')
        self.angle = 0
        self.sun.color('yellow')
        sunRadius = 50
        self.sunRadiusFromOrigin = 150
        self.sun.setpos(0,self.sunRadiusFromOrigin)
        self.sun.begin_poly()
        self.sun.pendown()
        self.sun.begin_fill()
        self.sun.circle(sunRadius)
        self.sun.end_poly()
        self.sun.end_fill()
        self.sun.penup()
        self.polyColorDics.append({"poly":self.sun.get_poly(),"color":"yellow"})
        self.startingPoly = self.polyColorDics[0]['poly']
        self.angle = 0
        Sun.suns.append(self.sun.get_poly())

    def getTime(self):
        return (((self.angle/360)*1440)+(12*60))%(60*24)
        
    #@Override
    def move(self):
        self.angle = self.angle%360
        self.angle -= self.amtToRotate
        self.polyColorDics[0]['poly'] = tuple(rotateAroundPoint(x,(0,0),self.angle) for x in self.startingPoly)
        Sun.suns.append(self.polyColorDics[0]['poly'])
        self.polyColorDics = [self.polyColorDics[0]] #remove all stars
        if self.getTime()<(5*60)+30 or self.getTime()>(24*60)-((5*60)+30):
            for _ in range(3):
                starCoordsX = random.randint(rangeSky['x']['lower'],rangeSky['x']['upper'])
                starCoordsY = random.randint(0,rangeSky['y']['upper'])
                starCoords = (starCoordsX,starCoordsY)
                poly = (starCoords,(starCoords[0],starCoords[1]+1),(starCoords[0]+1,starCoords[1]+1),(starCoords[0]+1,starCoords[1]))
                self.polyColorDics.append({'poly':poly,'color':'white'})

    def clearDrawing(self):
        self.sun.clear()


def isValidColor(r,g,b)->bool:
    return all(x>=0 and x<=255 for x in (r,g,b))


def getSkyColor(time:'mins'):
    fiveOClock = (5*60)
    sixOClock = (6*60)
    sevenOClock = (7*60)
    eightOClock = (8*60)
    day = 60*24
    increment = 60  #mins
    if time>=day-fiveOClock or time<fiveOClock:
        return (0,0,0) #black ie night
    
    elif (time>=fiveOClock and time<sixOClock) or (time>=day-sixOClock and time<day-fiveOClock):
        gradient = (time-fiveOClock)/increment if time<sixOClock else (day-fiveOClock-time)/increment
        return (int(255*gradient),0,0) #approaching red
    
    elif (time>=sixOClock and time<sevenOClock) or (time>=day-sevenOClock and time<day-sixOClock):
        gradient = (time-sixOClock)/increment if  time<sevenOClock else (day-sixOClock-time)/increment
        return (255,int(255*gradient*0.5),0) #approaching orange
    
    elif (time>=sevenOClock and time<eightOClock) or (time>=day-eightOClock and time<day-sevenOClock):
        gradient = (time-sevenOClock)/increment if time<eightOClock else (day-sevenOClock-time)/increment
        decreasing = int(255*(1-gradient))
        return (decreasing,int(decreasing*0.5),int(255*gradient)) #approaching blue
    
    else:
        # it's 8:00 - 4:00
        return (0,0,255) #blue

if __name__ == "__main__":
    screen.colormode(255)
    numMountains=3
    numFlowers=7
    numClouds=3
    numBirds = 3
    sun = Sun()
    Ground()
    for _ in range(numMountains):
        Mountain()
    for _ in range(numClouds):
        Cloud()
    for _ in range(numFlowers):
        Flower()
    for _ in range(numBirds):
        Bird()
    turt = turtle.Turtle()
    turt.speed('fastest')
    turt.hideturtle()
    turt.seth(90)
    turt.shape(AnimatedObject.getShape())
    turt.showturtle()
    AnimatedObject.clearDrawingAll()
    input()
    while(1):
        AnimatedObject.moveAll()
        turt.shape(AnimatedObject.getShape())
        screen.bgcolor(getSkyColor(sun.getTime()))
        #print(sun.getTime())
    
