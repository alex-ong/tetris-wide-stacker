
import TetrisField
import LayoutCreator
import multiprocessing
from multiprocessing import cpu_count
import random
import itertools

from FieldEvaluator import PIECE_HEIGHT_SCORE,MAX_HEIGHT_SCORE,LINE_SCORE,BUMPINESS_SCORE,OTHER_PIECE_CONFORM_SCORE

def noFunc():
    pass

def scoreField(field):
    columnHeights = field.getColumnHeights()    
    score = -min(columnHeights)  # score is how many completed lines there are.
    return score

def EvaluateWeights(weights):
    field = TetrisField.TetrisField(15, 30)
    layout = LayoutCreator.LayoutCreator(field, noFunc, weights)
    layout.createLayout()
    score = scoreField(field)        
    return (weights, score)

def mutateIndex(weights, index):
    if index == PIECE_HEIGHT_SCORE:
        weights[index] += random.uniform(-0.002, 0.002)
    elif index == MAX_HEIGHT_SCORE:
        weights[index] += random.uniform(-0.002, 0.002)
    elif index == LINE_SCORE:
        weights[index] += random.uniform(-0.002, 0.002)
    elif index == BUMPINESS_SCORE:
        weights[index] += random.uniform(-0.002, 0.002)
    elif index == OTHER_PIECE_CONFORM_SCORE:
        weights[index] += random.uniform(-0.020, 0.020)
        
def getMutators(bestIndividuals):
    result = []
    for weights in bestIndividuals:
        for i in range(len(weights)):
            newResult = weights.copy()
            mutateIndex(newResult, i)
            result.append(newResult)
    return result

# returns all pairs of items. e.g.:
# [a,b,c]
# (a, b) (a,c)
# (b, a) (b,c)
# (c, a) (c,b) 
def all_pairs(lst):
    return itertools.permutations(lst, 2)

# simple 1 element crossover.        
def getCrossover(bestIndividuals):
    results = []    
    for pair in all_pairs(bestIndividuals):
        left, right = pair
        for index, weight in enumerate(right):            
            if left[index] != weight: #quick redundancy check.
                newResult = pair[0].copy()
                newResult[index] = weight
                results.append(newResult)
    return results

baseWeights = [0.8677493555073127, 0.97453014898381, 1.0178958787096912, 0.9315999576603519, 5.0] 
bestIndividualSize = 5    
iterations = 100
current_iteration = 0
            
if __name__ == '__main__':
    cpu_count = max(1, multiprocessing.cpu_count() - 1)
    pool = multiprocessing.Pool(cpu_count)
    
    # 1. Initialize Population
    allWeights = [baseWeights.copy(), baseWeights.copy()] # population of 2.
     
    # 2. Evaluate population
    results = pool.map(EvaluateWeights, allWeights)
    
    # 3. while (!stopcondition) do:
    while current_iteration < iterations:        
        # 4. select best-fit individuals for reproduction
        sorted(results, key=lambda result: result[1], reverse=True)    
        results = results[:bestIndividualSize]
        bestIndividuals = results[:]
        bestIndividuals = [item[0] for item in bestIndividuals] #get weights only.
        
        # 5. breed new individuals through crossover and mutation
        # 5.1 breed via mutation.
        mutators = getMutators(bestIndividuals)        
        # 5.2 breed via crossover
        crossovers = getCrossover(bestIndividuals)         
        # 6. evaluate the individual fitness of new individuals
        childWeights = mutators + crossovers
        childResults = pool.map(EvaluateWeights, childWeights)
        # 7. replace least-fit population with new individuals. 
        results += childResults
        
        current_iteration += 1
        print ("Iteration" + str(current_iteration) + str(results[0]))
        
