# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 22:42:23 2019

@author: nguyen truong
"""

import math


from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

#refer and modify from this source: https://introcs.cs.princeton.edu/python/33design/vector.py.html
class Vector:
    def __init__(self, array):
        if (len(array) != 3):
            raise Exception("Only support vector of length 3")
        self._array = array
    
    def getNumDimensions(self):
        return len(self._array)
    
    def __getitem__(self, i):
        return self._array[i]
    
    def __add__(self, other):
        return Vector([i+j for i, j in zip(self._array, other._array)])
    
    def __sub__(self, other):
        return Vector([i-j for i, j in zip(self._array, other._array)])
    
    def __abs__(self):
        return math.sqrt(self.dot(self))
    
    def __str__(self):
        return str(self._array) 
    
    def dot(self, other):
        r = 0
        for i, j in zip(self._array, other._array): r += i*j
        return r
    
    def scale(self, scalar):
        return Vector([cor * scalar for cor in self._array])
    
    def getUnitVector(self):
        return self.scale(1.0/abs(self))
    
    def distanceTo(self, other):
        dVector = self - other
        return abs(dVector)
    
    def getUnitDirectionVectorFrom(self, other):
        dVector = other - self
        return dVector.getUnitVector()
        #return d.scale(1.0/self.distanceTo(other))
    
     
#refer and modify from this source: https://introcs.cs.princeton.edu/python/34nbody/body.py.html 
class Body:
    G = 6.67 * 10 ** (-11)
    AU = 149597870700
    def __init__(self, initPos, mass, initV, name = "undefined"):
        self.pos = initPos # this should be a point, but for the convenience we need to pass in our defined vector
        self.m = mass # a number
        self.v = initV # a vector
        self.name = name
    
    def getName(self):
        return self.name
    
    def getPos(self):
        return self.pos
    
    def getPosInAU(self):
        return self.getPos().scale(1/Body.AU)
    
    def getMass(self):
        return self.m
    
    def getV(self):
        return self.v
    
    def getForceVectorFrom(self, other):
        F = Body.G * self.m * other.m / (self.pos.distanceTo(other.pos)**2)
        return self.pos.getUnitDirectionVectorFrom(other.pos).scale(F)

    def __getAccelerationVector(self, f):
        return f.scale(1/self.m)
    
    def __updateVelocity(self, f, dt):
        self.v += self.__getAccelerationVector(f).scale(dt)
    
    def __updatePos(self, f, dt):
        self.pos +=  self.v.scale(dt)
        
    def move(self, f, dt):
        self.__updateVelocity(f, dt)
        self.__updatePos(f, dt)
        
        
    def __str__(self):
        return f'name: {self.name}; mass: {self.m}; cur_pos: {str(self.pos)}; cur_v: {str(self.v)}'

        
# calculate the total gravitational force on each of the N bodies
# return a list of vector, where the ith element is the total force (as a vector) on body i.
def calculate_each_body_total_gForce(bodies):
    listToReturn = []
    for time in range(len(bodies)):
        firstBody = bodies[0]
        del bodies[0]
        totalForce = Vector([0, 0, 0])
        for body in bodies:
            totalForce += firstBody.getForceVectorFrom(body)
        bodies.append(firstBody)
        listToReturn.append(totalForce)
    
    #debugging    
    #for force in listToReturn:
    #    print(force)
    return listToReturn

    
# move each of the N bodies at t timestep (at default set to 1)
# return the new postion list (in AU -- Astronomical Unit), then the new velocity list
def move_each_body(bodies, dt=1):
    curForceOnEachBody = (calculate_each_body_total_gForce(bodies))
    #positions of all bodies in AU unit
    positionsInAU = []
    #velocities of all bodies
    velocities = []
    
    for i in range(len(bodies)):
        #move the body i-th
        bodies[i].move(curForceOnEachBody[i], dt)
        #append information to the lists
        positionsInAU.append(bodies[i].getPosInAU())
        velocities.append(bodies[i].getV())
    
    #debugging
    #for body in bodies:
        #print("name: " + body.getName() + ", cur_pos: " + str(body.getPosInAU()))
    return positionsInAU, velocities

# refer and modify from: https://gist.github.com/benrules2/856d4151573a1408eac23da83851495f
def plot(listOfBodyToVectorsMaps):
    fig = plt.figure(figsize=(20,10))
    
    ax = fig.gca(projection='3d')
    
    ax = fig.add_subplot(1,1,1, projection='3d')
    colors = []
    
    for eachMap in listOfBodyToVectorsMaps:
        label = eachMap["name"]
        positions = eachMap["positions"]
        color = list(np.random.choice(range(256), size=3)).append(1)
        
        #ensure unique color
        while color in colors:
            list(np.random.choice(range(256), size=3)).append(1)
        
        xdata = []
        ydata = []
        zdata = []
        
        for eachPos in positions:
            xdata.append(eachPos[0])
            ydata.append(eachPos[1])
            zdata.append(eachPos[2])
        

        ax.plot(xdata, ydata, zdata, c = color, label = label)        
    

    ax.legend()
    elevDeg, azimDeg= 40, 0
    print('===GRAPH CONFIG===')
    print(f'elevation: {elevDeg} deg; azimuth: {azimDeg} deg')
    print('==================')
    ax.view_init(elevDeg, azimDeg)    
    plt.show()
    
                
def main():
    
    duration, timeStep = 0, 0
    bodies = []
    again = 'y'
    while again != 'n':
        
        #data from Wikipedia
        sun = {"initPos": Vector([0.0, 0.0, 0.0]), "mass": 1.99 * (10**30), "initV": Vector([0.0, 0.0, 0.0]), "name": "Sun"}
        mercury = {"initPos": Vector([0.0, 63.82 * (10**9), 0.0]), "mass": 3.29 * (10**23), "initV": Vector([47362.0, 0.0, 0.0]), "name": "Mercury"}
        venus = {"initPos": Vector([0.0, 108.89 * (10**9), 0.0]), "mass": 4.867 * (10**24), "initV": Vector([35020.0, 0.0, 0.0]), "name": "Venus"}
        earth = {"initPos": Vector([0.0, 149.65 * (10**9), 0.0]), "mass": 5.97 * (10**24) , "initV": Vector([29780.0, 0.0, 0.0]), "name": "Earth"}
        mars = {"initPos": Vector([0.0, 242.43 * (10**9), 0]), "mass": 6.39 * (10**23), "initV": Vector([24000.00, 0.0, 0.0]), "name": "Mars"}
        jupiter = {"initPos":Vector([0.0, 783.44 * (10**9), 0.0]), "mass": 1.90 * (10**27) , "initV": Vector([13070, 0.0, 0.0]), "name": "Jupiter"}
        saturn = {"initPos":Vector([0.0, 1.4986 * (10**12), 0.0]), "mass": 5.68 * (10**26), "initV": Vector([9680, 0.0, 0.0]), "name": "Saturn"}
        uranus = {"initPos":Vector([0.0, 2.9653 * (10**12), 0.0]), "mass": 8.681 * (10**25) , "initV": Vector([6800, 0.0, 0.0]), "name": "Uranus"}
        neptune = {"initPos":Vector([0.0, 4.4773 * (10**12),0.0]), "mass": 1.02 * (10**26), "initV": Vector([5430, 0.0, 0.0]), "name": "Neptune"}
        
        
        question1Bodies = [
                Body(Vector([0, 0, 0]), earth["mass"], Vector([0, 0, 0]), earth["name"]),
                Body(Vector([0.0, 384.44 * (10**6) ,0.0]), 7.35 * (10**22), Vector([1022.0, 0.0, 0.0]), "moon")
        ]

        question2Bodies = [
                Body(sun["initPos"], sun["mass"], sun["initV"], sun["name"]),
                Body(earth["initPos"], earth["mass"], earth["initV"], earth["name"])
        ]
    
        
        question3Bodies = [
                Body(sun["initPos"], sun["mass"], sun["initV"], sun["name"]),
                Body(mercury["initPos"], mercury["mass"], mercury["initV"], mercury["name"]),
                Body(venus["initPos"], venus["mass"], venus["initV"], venus["name"]),
                Body(earth["initPos"], earth["mass"], earth["initV"], earth["name"]),
                Body(mars["initPos"], mars["mass"], mars["initV"], mars["name"]),
                Body(jupiter["initPos"], jupiter["mass"], jupiter["initV"], jupiter["name"]),
                Body(saturn["initPos"], saturn["mass"], saturn["initV"], saturn["name"]),
                Body(uranus["initPos"], uranus["mass"], uranus["initV"], uranus["name"]),
                Body(neptune["initPos"], neptune["mass"], neptune["initV"], neptune["name"])  
        ]
        
        listOfBodyToVectorsMaps = []
        
        print('Please choose which movement you want to observe:')
        print('1. Movement of the Moon around the Earth.')
        print('2. Movement of the Earth around the Sun.')
        print('3. Movement of all planets around the Sun in the solar system.')
        
        questionNum = int(input('Enter question: '))
        
        while questionNum not in range(1, 4):
            print("Invalid input. Please enter again.")
            questionNum = int(input('Enter questions: '))
        
        if (questionNum  == 1):
            bodies = question1Bodies
            days = int(input('Enter number of days: '))
            duration, timeStep = days*86400, 100 #86400s = 1day, and choose dt=100
            
        elif (questionNum == 2):
            bodies = question2Bodies
            days = int(input('Enter number of days: '))
            duration, timeStep = days*86400, 100 #86400s = 1day, and choose dt=100
            
        elif (questionNum == 3):
            bodies = question3Bodies
            numYear = int(input('Enter a small number of years (<100): ')) 
            duration, timeStep = numYear*31104000 , 1800 #31104000s = 1year, and 1800s = 30 min
        
            #this following setting is for 6 months, need to comment the prev settings out
            #duration, timeStep = 2592000*6 , 100
        
        
        #simulation goes here
        for body in bodies:
            listOfBodyToVectorsMaps.append({"name" : body.getName(), "positions": []})
            
        for time in range(0, duration, timeStep):
            positionsInAU, velocities = move_each_body(bodies, timeStep)
            for bodyIndex in range(len(bodies)):
                    listOfBodyToVectorsMaps[bodyIndex]["positions"].append(positionsInAU[bodyIndex])
            
        plot(listOfBodyToVectorsMaps) 
        
        
        again = input("Continue? [y/n] ")
        again = again.lower()
        while again not in ['y', 'n']:
            print('y/n only!')
            again = input("Continue? [y/n] ")
        
main()

    
    


    
        