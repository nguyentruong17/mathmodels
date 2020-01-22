In this project, I implemented a Markov transition matrix to reveal the frequencies of each 'estate' in the game Monopoly. Hence, the word 'Markovopoly' :D <br />
<br />
Until line 240, I tried to simulate the states of movement in one round of monopoly. The 'states' here simply means how many doubles you've rolled before -- 0-doubled, or 1-doubled, or 2-doubled state. Then, I multiplied the result matrix with itself for 10000 times (and the matrix reaches its steady state) to find the frequencies. <br />
The game also assumes that if you roll 3 doubles in a row, you'll go to jail and the only ways to get out of jail are: <br /> 
1) you roll a double --> you'll move that many squares out of the jail square immediately; <br /> 
2) you have stayed in jailed for 2 turns, and your third turn will get you out of jail no matter the outcome of the roll and make you move that many squares out of the jail square <br />
<br />
Hopefully after running this Python program, you'll have a better strategy to invest in your next Monopoly game! <br />
P/S: for Vietnamese fans of this game, you can also switch this to Vietnamese version by simple uncommenting line 265 and commenting line 268. 'Own it all'!

