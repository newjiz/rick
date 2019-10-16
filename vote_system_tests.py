import numpy
import random
import math
import statistics


NUM_CONTENT = 1000
NUM_VOTES = 1000000

#parameters
par_logistic_scale = 200
par_elo_n = 100
par_elo_k = 40

#aqui es pot jugar amb n i k per aconseguir millors resultats, depenent del nombre de continguts i del nombre de vots.
#https://blog.mackie.io/the-elo-algorithm
#per exemple en el ranking d'escacs, o de futbol, n=400. k varia entre 20 i 60 aprox depenent del cas



content = []

#First component is the "real" rating. Second is the algorithm's rating, starting at 0.
#We assume a logistic distribution (can be done with normal as well).

for i in range(NUM_CONTENT):
    content.append([numpy.random.logistic(0,par_logistic_scale),0])

#ELO algorithm.
for i in range(1,NUM_VOTES):
    players = random.sample(range(NUM_CONTENT),2)
    #E = expected probability of player 1 winning (from actual ratings)
    E = 1/(1 + math.exp(-(content[players[0]][1]-content[players[1]][1])/par_elo_n))
    #E_real = from real ratings 
    E_real = 1/(1 + math.exp(-(content[players[0]][0]-content[players[1]][0])/par_elo_n))
    rand = random.random()
    if rand < E_real:
        content[players[0]][1] += par_elo_k*(1-E)
        content[players[1]][1] += -par_elo_k*(1-E)
    else:      
        content[players[0]][1] += -par_elo_k*E
        content[players[1]][1] += par_elo_k*E


#compare the two orderings
originals = []   
for row in content:
    originals.append(row[0])   

actuals = []
for row in content:
    actuals.append(row[1])

order1 = sorted(range(NUM_CONTENT), key=lambda k: originals[k])
order2 = sorted(range(NUM_CONTENT), key=lambda k: actuals[k])

#Mean deviation and standard deviation
difference = 0
difference_quadr = 0
for i in range(NUM_CONTENT):
    difference += abs(content[i][0] - content[i][1])
    difference_quadr += (content[i][0] - content[i][1])*(content[i][0] - content[i][1])
difference /= NUM_CONTENT
difference_quadr /= NUM_CONTENT
difference_quadr = math.sqrt(difference_quadr)


#Ultra-inefficient distance algorithm (but I think this is the right distance to compare rankings)
#linear = mean difference,  quadratic = standard deviation 
distance_linear = 0
distance_quadr = 0
i = 0
for i in range(NUM_CONTENT):
    for j in range(NUM_CONTENT):
        if order1[i] == order2[j]:
            distance_linear += abs(i-j)
            distance_quadr += (i-j)*(i-j)
distance_linear /= NUM_CONTENT
distance_quadr /= NUM_CONTENT
distance_quadr = math.sqrt(distance_quadr)

print('Mean deviation and standard deviation of the computed ELOs wrt the inner ELOs')
print(difference)
print(difference_quadr)

print('Mean deviation and standard deviation of the distance between the computed position and the real position')
print(distance_linear)
print(distance_quadr)
