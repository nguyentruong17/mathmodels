# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 10:58:12 2019

@author: nguyen truong
"""
from pylab import *
import matplotlib.pyplot as plt
import numpy as np

#initialize the monopoly matrix
#here we multiply 40 by 3 because we have 40 squares for the gameboard, 
#and each square is going to have 3 states. The states indicate the rolling status of the player:
#zero-doubled means the player haven't rolled no double before (or just got reset)
#one-doubled means the player haved rolled one double before
#two-doubled means the player haved rolled two double before

movingMatrix = mat(zeros((40*3, 40*3)))

#init the initial vector
initialVector = [0]*119
initialVector.insert(0, 1)

#make the array into vector
initialVector = mat((initialVector))


#initialize the list of moving probabilities
probListWithoutDouble = [0, 0, 0/36, 2/36, 2/36, 4/36, 4/36, 6/36, 4/36, 4/36, 2/36, 2/36, 0/36]
probListDoubleOnly    = [0, 0, 1/36, 0/36, 1/36, 0/36, 1/36, 0/36, 1/36, 0/36, 1/36, 0/36, 1/36]


listOfProbsZeroD = [probListWithoutDouble, probListDoubleOnly, [0] * 13] # at zero double, one can only go back to zero-doubled state or go to one-doubled state
listOfProbsOneD = [probListWithoutDouble, [0] * 13, probListDoubleOnly] # at one double, one can only go back to zero-doubled state or go to two-doubled state
listOfProbsTwoD = [probListWithoutDouble, probListDoubleOnly, [0] * 13] # at two double, one can only go back to zero-double state or go to jail if roll a double

#initialize the list of special squares -- community chest squares, community chest squares that lead to change square, and chance squares
#all of the loop represent the 3 states 
communityChestSquares = []
for i in range(3):
    communityChestSquares.append(2+40*i)
    communityChestSquares.append(17+40*i)
    communityChestSquares.append(33+40*i)

communityChestSquaresThatLeadToChanceSquare = []
for i in range(3):
    communityChestSquaresThatLeadToChanceSquare.append(33+40*i)
    
chanceSquares = []
for i in range(3):
    chanceSquares.append(7+40*i)
    chanceSquares.append(22+40*i)
    chanceSquares.append(36+40*i)

#find the nearest railroad square to the current square-which has to be the square of chance cards
def nearestRailRoad(curSquare):
    curSquare = curSquare %40
    reading = 5
    pen = 15
    bo = 25
    short = 35
    if (curSquare <= 10):
        return reading
    elif (curSquare <= 20):
        return pen
    elif (curSquare <= 30):
        return bo
    elif (curSquare < 40):
        return short
    
#find the nearest utility square to the current square-which has to be the square of chance cards
def nearestUtility(curSquare):
    curSquare = curSquare %40
    electric = 12
    water = 28
    if (curSquare == 7):
        return electric
    elif (curSquare == 22):
        return electric
    elif (curSquare == 36):
        return water

#takes chance and community cards into account
#there are 16 community cards and 16 change cards and we assume they're well shuffled at the end of each turn
        
def addMoreRules(matrix, row, col, startCol):
    
    probAtSquare = matrix[row, col]
    
    #go to chance squares:
    if (col in chanceSquares):
        
        #go to go square
        matrix[row, startCol+0] += probAtSquare * 1/16 
                 
        #go to illinois avenue
        matrix[row, startCol+24] += probAtSquare * 1/16
                 
        #go to nearest utility
        matrix[row, startCol+nearestUtility(col)] += probAtSquare * 1/16
                 
        #go to nearest railroad
        matrix[row, startCol+nearestRailRoad(col)] += probAtSquare * 2/16 #there are 2 of these 'go to the nearest railroads' chance cards
                 
        #move to st.charles place
        matrix[row, startCol+11] += probAtSquare * 1/16
                 
        #move back 3 spaces
        if (col in communityChestSquaresThatLeadToChanceSquare):
           matrix[row, startCol+0] += probAtSquare * 1/16 *1/16
           matrix[row, 30] += probAtSquare * 1/16 * 1/16
           matrix[row, col-3] += probAtSquare * 1/16 * 14/16
           
        else:
           matrix[row, col-3] += probAtSquare * 1/16
                
        #go to jail:
        matrix[row, 30] += probAtSquare * 1/16

        #go to reading rail road
        matrix[row, startCol+5] += probAtSquare * 1/16
                
        #go to boardwalk
        matrix[row, startCol+39] += probAtSquare * 1/16
                 
                 
        #decrease the prob at staying
        #there are 6 chance cards that doesn't transport the player to somewhere else
        matrix[row, col] = probAtSquare * 6/16
                
                     
                 
    #go to community chest squares    
    elif (col in communityChestSquares):
        #go to jail:
        matrix[row, 30] += probAtSquare * 1/16
            
        #go to start
        matrix[row, startCol+0] += probAtSquare * 1/16
        
        #decrease the prob at staying
        #there are 14 community chest cards that doesn't transport the player to somewhere else
        matrix[row, col] = probAtSquare * 14/16

## go to jail prob = go to square 30 prob

## when to go to jail?
# the die leads to jail
# double thrice
# community chest

## rule: go to 30 0d = go to jail
### at 30 0d = just arrived at jail
### at 30 1d = in jail for 1 turn
### at 30 2d = in jail for 2 turns


## when to get out of jail?
# have double
# stay in jail twice, the third rolling gets you out, start going from square 10


## at 0 double state
# can only go to 0 or 1 double state
# special case: at square 30, if double, go from 10 of state 0 double; else; move to 30 1 double
for row in range(40):
    for state in range(len(listOfProbsZeroD)):
        startCol = state * 40 #startCol is 0, 40, and 80
        probListToUse = listOfProbsZeroD[state]
        for numSteps in range(len(probListToUse)):
             if (row == 30): # in jail for 1 turn
                if (state == 0): #not double
                    col = 70 # move to square 30 of 1 double (1*40 + 30)
                elif (state == 1): #roll double
                    col = 10 + numSteps # move numStep squares after square 10 of 0 double
             else:
                col =  (row%40 + numSteps) % 40 + startCol #if x >=40/80/120, then makes x starts again at 0/40/80
                
                    
             movingMatrix[row, col] += probListToUse[numSteps]
             
             #uncomment this for disabling the community chest and chance cards
             addMoreRules(movingMatrix, row, col, startCol)
             
        

## at 1 double state
# can only go to 0 or 2 doubles state
# special case: at square 70, if double, go from 10 of state 0 double; else; move to 30 2 double
for row in range(40, 80):
    for state in range(len(listOfProbsOneD)):
        startCol = state * 40 #startCol is 0, 40, and 80
        probListToUse = listOfProbsOneD[state]
        for numSteps in range(len(probListToUse)):
                      

            if (row == 70): # in jail for 2 turns
                if (state == 0): #not double
                    col = 110 # move to square 30 of 2 doubles (2*40 +30)
                    
                    
                elif (state == 2): #roll double
                    col = 10 + numSteps # move numStep squares after square 10 of 0 double
                    
                #print(state, row, col, numSteps, probListToUse[numSteps])
                
            else:
                col = (row%40 + numSteps) % 40 + startCol #if x >=40/80/120, then makes x starts again at 0/40/80
            
            movingMatrix[row, col] += probListToUse[numSteps]
            
            #uncomment this for disabling the community chest and chance cards
            addMoreRules(movingMatrix, row, col, startCol)
            
            
    
## at 2 doubles state
#can only go to 0 double state
# special case: at square 110, go from 10 of state 0 double; 
for row in range(80, 120):
    for state in range(len(listOfProbsTwoD)):
        startCol = state * 40 #startCol is 0, 40, and 80
        probListToUse = listOfProbsTwoD[state]
        for numSteps in range(len(probListToUse)):
            if (row == 110): #in jaill for the last turn
                col = 10 + numSteps # move numStep squares after square 10 of 0 double
            else:
                if (state == 1 ): #roll double again
                    col = 30 # go to jail
                else:    
                    col = (row%40 + numSteps) % 40 + startCol #if x >=40/80/120, then makes x starts again at 0/40/80
            movingMatrix[row, col] += probListToUse[numSteps]
            
            #uncomment this for disabling the community chest and chance cards
            addMoreRules(movingMatrix, row, col, startCol)



#raise the matrix to a very big power
movingMatrix = movingMatrix ** 10000

#debugging purpose -- sum of each row should be (close to) 1
#for row in range(120):
#    sumRow = 0
#    for col in range(120):
#        sumRow += movingMatrix[row, col]
#    print(sumRow)

#get the result vector
resultVector = initialVector.dot(movingMatrix)    

#find probability of each square from the result vector
allProbs = [0]*40
for state in range(3):
    for col in range(40):
        allProbs[col] += resultVector[0, col + 40*state]


#let's see the result!

#adding the name of each square
names = []

#this one for viet version
with open("square_names_vie.txt", "r", encoding="utf8") as file:

#this one for us version    
#with open("square_names_eng.txt", "r") as file:
    for line in file:
        names.append(line.strip())
print(len(names))

#adding the overall monopolies
brown = [1, 3]
lightBlue= [6, 8, 9]
pink = [11, 13, 14]
orange = [16, 18, 19]
red = [21, 23, 24]
yellow = [26, 27, 29]
green = [31, 32, 34]
darkBlue = [37, 39] 
monopoliesMap = {
        'Brown':brown,
        'Light Blue':lightBlue, 
        'Pink':pink, 
        'Orange':orange, 
        'Red':red, 
        'Yellow':yellow, 
        'Green':green, 
        'Dark Blue':darkBlue
        }

def findOverallMonopoly(curSquare):
    for each in monopoliesMap:
        if curSquare in monopoliesMap[each]:
            return each
    return 'None'

monopolies = []
for i in range(40):
    monopolies.append(findOverallMonopoly(i))
    

#print all prob of each square
print('ALL PROBABILITIES')
print('Square #  |'+'|  Probability  |'+'|  Monopoly  |'+'|  Square Name')
for i in range(len(allProbs)):
    print(f'{i:8}      {allProbs[i]:0.9f}      {monopolies[i]:10}      {names[i]}')
print('\n\n')

sortedGameTuple = sorted(zip([i for i in range(40)], allProbs, monopolies, names), key=lambda tup: tup[1], reverse=True)
top10 = sortedGameTuple[:10]
bottom10 = sortedGameTuple[-10:]

print('10 MOST LIKELY SQUARES')
print('Square #  |'+'|  Probability  |'+'|  Monopoly  |'+'|  Square Name')
for i in range(len(top10)):
    print(f'{top10[i][0]:8}      {top10[i][1]:0.9f}      {top10[i][2]:10}     {top10[i][3]}')
print('\n\n')

print('10 LEAST LIKELY SQUARES')
print('Square #  |'+'|  Probability  |'+'|  Monopoly  |'+'|  Square Name')
for i in range(len(bottom10)):
    print(f'{bottom10[i][0]:8}      {bottom10[i][1]:0.9f}      {bottom10[i][2]:10}     {bottom10[i][3]}')
print('\n\n')

print('PROBABILITY BY MONOPOLY')
monopoliesProb = []
monopoliesNames = []
curMonopoly = ''
for index in range(len(monopolies)):
    if (monopolies[index] != 'None'):
        if (monopolies[index] == curMonopoly):
            monopoliesProb[len(monopoliesProb)-1] += allProbs[index]
        else:
            curMonopoly=monopolies[index]
            monopoliesProb.append(allProbs[index])
            monopoliesNames.append(curMonopoly)
print('Probability  |'+'|  Monopoly')
for i in range(len(monopoliesProb)):
    print(f'{monopoliesProb[i]:0.9f}      {monopoliesNames[i]}')
print('\n\n')

#graph
y_pos = np.arange(len(names))
plt.figure(figsize=(15,5))
colors=[]
for index in range(len(monopolies)):
    each = monopolies[index]
    if each == 'Brown':
        colors.append('brown')
    elif each == 'Light Blue':
        colors.append('lightblue')
    elif each == 'Pink':
        colors.append('pink')
    elif each == 'Orange':
        colors.append('orange')
    elif each == 'Red':
        colors.append('red')
    elif each == 'Yellow':
        colors.append('yellow')
    elif each == 'Green':
        colors.append('green')
    elif each == 'Dark Blue':
        colors.append('darkblue')
    else:
        #railroads
        if (index in [5, 15, 25, 35]):
            colors.append('tan')
        #companies
        elif (index in [12, 28]):
            colors.append('plum')
        else:
            colors.append('silver')
            
plt.bar(y_pos, allProbs, color=colors)

plt.xticks(y_pos, names, rotation=90)
plt.subplots_adjust(bottom=0.4)
 
plt.title("Probability Of \nGoing To All Squares \nOn The Monopoly Gameboard")

    