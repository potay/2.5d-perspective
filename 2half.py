from Animation import *
import copy, math

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

def getAverage(L):
    average = float(sum(L))/len(L) if len(L) > 0 else float('NaN')
    return average

class Struct:
    pass

# The main World class.
# Instantiate the actual world/environment the user perceives.
class World(Animation):
    def init(self):
        # We seperate the world from the screen. The world is the virtual world
        # the objects are living in. The screen is the screen through which the
        # user views the world.

        # Set the resolution of the screen.
        self.yResolution = self.height
        self.xResolution = self.width

        # Set the origin x,y,z coordinates in the world.
        self.xCenter = float(self.xResolution)/2
        self.yCenter = float(self.yResolution)/2
        self.zCenter = 400.0

        # The assumed distance the user is from the screen. This is set to 1
        # for convenient math.
        self.screenDist = 1
        self.xFOV = 60.0 # Horizontal field of view in degrees.
        self.yFOV = 37.5 # Vertical field of view in degrees.
        self.moveDistance = 50.0 # Distance moved every keypress
        self.rotationAngle = 5.0 # Angle of rotation every keypresssss

        # Defining the vector of where the user is set to be in the virtual
        # world.
        self.centerPoint = Matrix([[self.xCenter], [self.yCenter], [0.0]])

        # List of all the items in the world. All items are 2D shapes in the
        # 3D world which will then be translated (non-destructively) into a 3D
        # object and drawn.
        self.itemList = []

        """Versions of the map"""
        # self.map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        #             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        self.map = [[1,1,0,1],
                    [1,0,0,1],
                    [1,0,1,1],
                    [1,0,1,1]]

        # Based on the Map, this iteratively creates a square instance for each
        # object and adds them to the item list.
        self.blockWidth = 400
        self.blockDepth = 400
        self.blockHeight = 400
        self.mapBlockWidth = len(self.map[0])
        self.mapBlockDepth = len(self.map)
        self.mapBlockHeight = 1

        for i in xrange(len(self.map)):
            for j in xrange(len(self.map[0])):
                blkDistFromC = (j-self.mapBlockWidth/2, 0, i-self.mapBlockDepth/2)
                blockCenter = Matrix([[self.xCenter+blkDistFromC[0]*self.blockWidth],
                    [self.yCenter+blkDistFromC[1]*self.blockHeight],
                    [self.zCenter+blkDistFromC[2]*self.blockDepth]])
                #print blockCenter

                if (self.map[i][j] == 1):
                    # Left Wall
                    item = Struct()
                    item.color = (100,200,100)
                    item.item = Square(self.canvas,
                    [blockCenter + Matrix([[-self.blockWidth/2], [-self.blockHeight/2], [-self.blockDepth/2]]),
                     blockCenter + Matrix([[-self.blockWidth/2], [-self.blockHeight/2], [self.blockDepth/2]]),
                     blockCenter + Matrix([[-self.blockWidth/2], [self.blockHeight/2], [self.blockDepth/2]]),
                     blockCenter + Matrix([[-self.blockWidth/2], [self.blockHeight/2], [-self.blockDepth/2]])])
                    self.itemList.append(item)

                    # Right Wall
                    item = Struct()
                    item.color = (100,200,100)
                    item.item = Square(self.canvas,
                    [blockCenter + Matrix([[self.blockWidth/2], [-self.blockHeight/2], [-self.blockDepth/2]]),
                     blockCenter + Matrix([[self.blockWidth/2], [-self.blockHeight/2], [self.blockDepth/2]]),
                     blockCenter + Matrix([[self.blockWidth/2], [self.blockHeight/2], [self.blockDepth/2]]),
                     blockCenter + Matrix([[self.blockWidth/2], [self.blockHeight/2], [-self.blockDepth/2]])])
                    self.itemList.append(item)

                    # Front Wall
                    item = Struct()
                    item.color = (200,100,100)
                    item.item = Square(self.canvas,
                    [blockCenter + Matrix([[-self.blockWidth/2], [-self.blockHeight/2], [self.blockDepth/2]]),
                     blockCenter + Matrix([[self.blockWidth/2], [-self.blockHeight/2], [self.blockDepth/2]]),
                     blockCenter + Matrix([[self.blockWidth/2], [self.blockHeight/2], [self.blockDepth/2]]),
                     blockCenter + Matrix([[-self.blockWidth/2], [self.blockHeight/2], [self.blockDepth/2]])])
                    self.itemList.append(item)

                    # Back Wall
                    item = Struct()
                    item.color = (200,100,100)
                    item.item = Square(self.canvas,
                    [blockCenter + Matrix([[-self.blockWidth/2], [-self.blockHeight/2], [-self.blockDepth/2]]),
                     blockCenter + Matrix([[self.blockWidth/2], [-self.blockHeight/2], [-self.blockDepth/2]]),
                     blockCenter + Matrix([[self.blockWidth/2], [self.blockHeight/2], [-self.blockDepth/2]]),
                     blockCenter + Matrix([[-self.blockWidth/2], [self.blockHeight/2], [-self.blockDepth/2]])])
                    self.itemList.append(item)

                    # Top Wall
                    item = Struct()
                    item.color = (100,100,200)
                    item.item = Square(self.canvas,
                    [blockCenter + Matrix([[-self.blockWidth/2], [-self.blockHeight/2], [self.blockDepth/2]]),
                     blockCenter + Matrix([[self.blockWidth/2], [-self.blockHeight/2], [self.blockDepth/2]]),
                     blockCenter + Matrix([[self.blockWidth/2], [-self.blockHeight/2], [-self.blockDepth/2]]),
                     blockCenter + Matrix([[-self.blockWidth/2], [-self.blockHeight/2], [-self.blockDepth/2]])])
                    self.itemList.append(item)

                # Bottom Wall
                item = Struct()
                item.color = (100,100,200)
                item.item = Square(self.canvas,
                [blockCenter + Matrix([[-self.blockWidth/2], [self.blockHeight/2], [self.blockDepth/2]]),
                 blockCenter + Matrix([[self.blockWidth/2], [self.blockHeight/2], [self.blockDepth/2]]),
                 blockCenter + Matrix([[self.blockWidth/2], [self.blockHeight/2], [-self.blockDepth/2]]),
                 blockCenter + Matrix([[-self.blockWidth/2], [self.blockHeight/2], [-self.blockDepth/2]])])
                self.itemList.append(item)

        # item = Struct()
        # item.color = (100,200,100)
        # item.item = Square(self.canvas,
        #     [Matrix([[self.xCenter-100], [self.yCenter-100], [500.0]]),
        #      Matrix([[self.xCenter+100], [self.yCenter-100], [500.0]]),
        #      Matrix([[self.xCenter+100], [self.yCenter+100], [500.0]]),
        #      Matrix([[self.xCenter-100], [self.yCenter+100], [500.0]])])
        # self.itemList.append(item)
        # item = Struct()
        # item.color = (100,200,100)
        # item.item = Square(self.canvas,
        #     [Matrix([[self.xCenter-100], [self.yCenter-100], [300.0]]),
        #      Matrix([[self.xCenter-100], [self.yCenter-100], [500.0]]),
        #      Matrix([[self.xCenter-100], [self.yCenter+100], [500.0]]),
        #      Matrix([[self.xCenter-100], [self.yCenter+100], [300.0]]),])
        # self.itemList.append(item)
        # item = Struct()
        # item.color = (100,200,100)
        # item.item = Square(self.canvas,
        #     [Matrix([[self.xCenter+100], [self.yCenter-100], [500.0]]),
        #      Matrix([[self.xCenter+100], [self.yCenter-100], [300.0]]),
        #      Matrix([[self.xCenter+100], [self.yCenter+100], [300.0]]),
        #      Matrix([[self.xCenter+100], [self.yCenter+100], [500.0]])])
        # self.itemList.append(item)

    # This method arranges the items in the item list from furthest to nearest
    # so that the items are drawn in that order.
    # It is buggy.
    def arrangeItems(self, component=2):
        def itemCmp(x, y):
            return -cmp((x.item.getCenter()-self.centerPoint).getMagnitude(),
                        (y.item.getCenter()-self.centerPoint).getMagnitude())

        self.itemList = sorted(self.itemList, itemCmp)

    # Returns resultant vector of the original vector projected on the screen.
    def getPerspectiveCoords(self, vector):
        vector = vector - Matrix([[self.xCenter], [self.yCenter], [0]])
        x, y, z = (getAverage(vector.getX()),
                   getAverage(vector.getY()),
                   getAverage(vector.getZ()))
        xMax = z * float(math.tan(self.xFOV/2/180*math.pi))
        xDist = float(x)/xMax*self.xResolution/2
        yMax = z * float(math.tan(self.yFOV/2/180*math.pi))
        yDist = float(y)/yMax*self.yResolution/2
        return Matrix([[self.xCenter+xDist], [self.yCenter+yDist], [z]])

    # Draws each item on the canvas with projection.
    def drawWithPerspective(self, item):
        item = copy.deepcopy(item)

        """Old methods"""
        # xMax = item.zWorld * math.tan(self.xFOV/2/180*math.pi)
        # xDist = item.xWorld/xMax*self.xResolution
        # yMax = item.zWorld * math.tan(self.yFOV/2/180*math.pi)
        # yDist = item.yWorld/yMax*self.yResolution
        # item.item.coords[0] = [self.xCenter+xDist-item.width/2, self.yCenter+yDist-item.height/2]
        # item.item.coords[1] = [self.xCenter+xDist+item.width/2, self.yCenter+yDist-item.height/2]
        # item.item.coords[2] = [self.xCenter+xDist+item.width/2, self.yCenter+yDist+item.height/2]
        # item.item.coords[3] = [self.xCenter+xDist-item.width/2, self.yCenter+yDist+item.height/2]

        # yCenter = (item.item.coords[3][1] + item.item.coords[0][1])/2
        # heightTop = (float(yCenter - item.item.coords[0][1])*self.screenDist/item.zWorld)
        # heightBottom = (float(item.item.coords[3][1] - yCenter)*self.screenDist/item.zWorld)
        # #print heightTop, heightBottom
        # item.item.coords[0][1] = yCenter - heightTop
        # item.item.coords[1][1] = yCenter - heightTop
        # item.item.coords[2][1] = yCenter + heightBottom
        # item.item.coords[3][1] = yCenter + heightBottom

        # xCenter = (item.item.coords[0][0] + item.item.coords[1][0])/2
        # widthLeft = (float(xCenter - item.item.coords[0][0])*self.screenDist/item.zWorld)
        # widthRight = (float(item.item.coords[1][0] - xCenter)*self.screenDist/item.zWorld)
        # #print heightTop, heightBottom
        # item.item.coords[0][0] = xCenter - widthLeft
        # item.item.coords[1][0] = xCenter + widthRight
        # item.item.coords[2][0] = xCenter + widthRight
        # item.item.coords[3][0] = xCenter - widthLeft

        item.item.coords = map(self.getPerspectiveCoords, item.item.coords)

        # isOutOfFrame checks to if item is in frame and only draws it then
        # to increase efficiency
        # Is buggy so < 5 is used to ignore it.
        if (item.item.isOutOfFrame(self.width, self.height) < 5 and
            getAverage(item.item.getCenter().getZ()) >= 100.0):
            item.item.draw(item.color)

    def drawAll(self):
        for item in self.itemList:
            self.drawWithPerspective(item)

    def redrawAll(self):
        self.drawAll()

    def keyPressed(self, event):
        if (event.keysym == "Down"):
            for item in self.itemList:
                for i in xrange(len(item.item.coords)):
                    item.item.coords[i] += Matrix([[0], [0], [self.moveDistance]])
        elif (event.keysym == "Up"):
            for item in self.itemList:
                for i in xrange(len(item.item.coords)):
                    item.item.coords[i] -= Matrix([[0], [0], [self.moveDistance]])
        elif (event.keysym == "Left"):
            for item in self.itemList:
                for i in xrange(len(item.item.coords)):
                    item.item.coords[i] += Matrix([[self.moveDistance], [0], [0]])
        elif (event.keysym == "Right"):
            for item in self.itemList:
                for i in xrange(len(item.item.coords)):
                    item.item.coords[i] -= Matrix([[self.moveDistance], [0], [0]])
        elif (event.char == "w"):
            for item in self.itemList:
                for i in xrange(len(item.item.coords)):
                    # Translates each item to the origin, rotates it about the
                    # axis and then translates it back.
                    center = self.centerPoint
                    item.item.coords[i] = item.item.coords[i] - center
                    item.item.coords[i] = Matrix([[1.0, 0, 0],
        [0, math.cos(self.rotationAngle/180*math.pi), math.sin(self.rotationAngle/180*math.pi)],
        [0, -math.sin(self.rotationAngle/180*math.pi), math.cos(self.rotationAngle/180*math.pi)]]) * item.item.coords[i]
                    item.item.coords[i] = item.item.coords[i] + center
        elif (event.char == "s"):
            for item in self.itemList:
                for i in xrange(len(item.item.coords)):
                    # Translates each item to the origin, rotates it about the
                    # axis and then translates it back.
                    center = self.centerPoint
                    item.item.coords[i] = item.item.coords[i] - center
                    item.item.coords[i] = Matrix([[1.0, 0, 0],
        [0, math.cos(self.rotationAngle/180*math.pi), -math.sin(self.rotationAngle/180*math.pi)],
        [0, math.sin(self.rotationAngle/180*math.pi), math.cos(self.rotationAngle/180*math.pi)]]) * item.item.coords[i]
                    item.item.coords[i] += center
        elif (event.char == "a"):
            for item in self.itemList:
                for i in xrange(len(item.item.coords)):
                    center = self.centerPoint
                    item.item.coords[i] = item.item.coords[i] - center
                    item.item.coords[i] = Matrix([[math.cos(self.rotationAngle/180*math.pi), 0, math.sin(self.rotationAngle/180*math.pi)],
                        [0, 1, 0],
                        [-math.sin(self.rotationAngle/180*math.pi), 0, math.cos(self.rotationAngle/180*math.pi)]]) * item.item.coords[i]
                    item.item.coords[i] += center
        elif (event.char == "d"):
            for item in self.itemList:
                for i in xrange(len(item.item.coords)):
                    center = self.centerPoint
                    item.item.coords[i] = item.item.coords[i] - center
                    item.item.coords[i] = Matrix([[math.cos(self.rotationAngle/180*math.pi), 0, -math.sin(self.rotationAngle/180*math.pi)],
                        [0, 1, 0],
                        [math.sin(self.rotationAngle/180*math.pi), 0, math.cos(self.rotationAngle/180*math.pi)]]) * item.item.coords[i]
                    item.item.coords[i] += center

        self.arrangeItems()

class Matrix(object):
    def __init__(self, matrix):
        self.matrix = matrix

    def __str__(self):
        string = "Matrix(["
        for row in self.matrix:
            string += str(row)
            if row != self.matrix[-1]:
                string += "\n"
        string += "])\n"
        return string

    def __repr__(self):
        string = "Matrix(%r)" % self.matrix
        return string

    def __add__(self, other):
        assert(len(self.matrix) == len(other.matrix) and len(self.matrix[0]) == len(other.matrix[0]))
        matrix = [[self.matrix[i][j]+other.matrix[i][j] for j in xrange(len(self.matrix[i]))] for i in xrange(len(self.matrix))]
        return Matrix(matrix)

    def __sub__(self, other):
        assert(len(self.matrix) == len(other.matrix) and len(self.matrix[0]) == len(other.matrix[0]))
        matrix = [[self.matrix[i][j]-other.matrix[i][j] for j in xrange(len(self.matrix[i]))] for i in xrange(len(self.matrix))]
        return Matrix(matrix)

    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            matrix = [[self.matrix[i][j]*other for j in xrange(len(self.matrix[i]))] for i in xrange(len(self.matrix))]
            return Matrix(matrix)
        else:
            assert(len(self.matrix[0]) == len(other.matrix))
            matrix = [[0]*len(other.matrix[0]) for i in xrange(len(self.matrix))]
            otherTransposed = zip(*other.matrix)
            for row in xrange(len(matrix)):
                for col in xrange(len(matrix[0])):
                    matrix[row][col] = reduce(lambda x,y: x+y, map(lambda (x,y): x*y, zip(self.matrix[row], otherTransposed[col])))
            return Matrix(matrix)

    def __rmul__(self, other):
        return self.__mul(other, self)

    def __copy__(self):
        return Matrix(self.matrix)

    def __deepcopy__(self, memo):
        return Matrix(copy.deepcopy(self.matrix))

    def getXYFromVector(self):
        return [self.matrix[0][0], self.matrix[1][0]]

    def getX(self):
        return self.matrix[0]

    def getY(self):
        return self.matrix[1]

    def getZ(self):
        return self.matrix[2]

    def getCenter(self):
        return Matrix([[getAverage(self.matrix[0])],
                       [getAverage(self.matrix[1])],
                       [getAverage(self.matrix[2])]])

    def transpose(self):
        return Matrix(zip(*self.matrix))

    def getMagnitude(self):
        rnVector = Matrix([[e] for item in (zip(*self.matrix)) for e in item])
        return getAverage((rnVector.transpose() * rnVector).getX()) ** 0.5


class Square(object):
    def __init__(self, canvas, coords):
        self.canvas = canvas
        self.coords = coords
        self.color = (100,100,200)

    def draw(self, color=None):
        if color==None: color = self.color
        coords = [coord.getXYFromVector() for coord in self.coords]
        shadowCoords = copy.deepcopy(coords)
        height = shadowCoords[3][1] - shadowCoords[0][1]
        width = shadowCoords[1][0] - shadowCoords[0][0]
        shadowCoords[0][1] = shadowCoords[3][1] + height*0.4
        shadowCoords[1][1] = shadowCoords[2][1] + height*0.4
        shadowCoords[0][0] = shadowCoords[0][0] - width*0.25
        shadowCoords[1][0] = shadowCoords[1][0] + width*0.25

        avgZ = getAverage([getAverage(self.coords[0].getZ()), getAverage(self.coords[1].getZ()), getAverage(self.coords[2].getZ()), getAverage(self.coords[3].getZ())])
        colorComponent = []
        for component in self.color:
            component = component-avgZ/10.0
            if (component > 255):
                component = 255
            elif (component < 0):
                component = 0
            colorComponent.append(component)
        color = rgbString(*colorComponent)

        #self.canvas.create_polygon(shadowCoords, fill='grey95')
        self.canvas.create_polygon(coords, fill=color)

    def isOutOfFrame(self, frameWidth, frameHeight):
        total = 0
        for coord in self.coords:
            #print coord.getX(), coord.getY()
            if (coord.getX() < 0 or coord.getX() > frameWidth or
               coord.getY() < 0 or coord.getY() > frameHeight):
                total += 1
        return total

    def __repr__(self):
        return "Square(%r, %r)" % (self.canvas, self.coords)

    def __copy__(self):
        return Square(self.canvas, self.coords)

    def __deepcopy__(self, memo):
        return Square(self.canvas, copy.deepcopy(self.coords))

    def getCenter(self):
        center = []
        for i in xrange(len(self.coords)):
            for j in xrange(len(self.coords[i].matrix)):
                if j >= len(center):
                    center.append(copy.deepcopy(self.coords[i].matrix[j]))
                else:
                    center[j].extend(copy.deepcopy(self.coords[i].matrix[j]))
        center = [[getAverage(component)] for component in center]
        return Matrix(center)

World().run(1440,900)
