
import TetrisField
import LayoutCreator
import multiprocessing
from multiprocessing import cpu_count
import random
import math

def noFunc():
    pass

def scoreField(field):
    columnHeights = field.getColumnHeights()    
    score = evaluateBumpiness(columnHeights)
    return score

def evaluateBumpiness(columnHeights):
    score = 0
    prevHeight = columnHeights[0]
    for i in range(1, len(columnHeights)):
        score += abs(prevHeight - columnHeights[i])
        prevHeight = columnHeights[i] 
    return score

def EvaluateWeights(weights):
    field = TetrisField.TetrisField(150, 15)
    layout = LayoutCreator.LayoutCreator(field, noFunc, weights)
    layout.createLayout()
    score = scoreField(field)    
    print (weights, score)
    return (weights, score)

def randomizeWeights(baseWeights):
    result = baseWeights.copy()
    for i in range(len(result)):
        if (math.fabs(result[i]) < 0.001):  # make sure we have "some" weight.
            result[i] = 0.01 
        result[i] += (random.uniform(-0.3, 0.3) * result[i])
    return result
        
def GenerateWeights(baseWeights):
    result = []
    for _ in range(12):
        result.append(baseWeights.copy())
    for _ in range(6):
        result.append(randomizeWeights(baseWeights))
    return result

def findNewBase(results):
    '''results are in the form (weights,score)'''
    results.sort(key=lambda tup: tup[1])  # we want lowest score.
    # average the first 5
    avgScore = 0.0
    finalResult = results[0][0].copy()
    for i in range(1, 5):
        (result, score) = results[i]
        for j in range(len(finalResult)):
            finalResult[j] += result[j]
        avgScore += score
            
    for j in range(len(finalResult)):
        finalResult[j] /= 5.0
    avgScore /= 5
    
    
    return (finalResult, avgScore)
            
if __name__ == '__main__':
    cpu_count = max(1, multiprocessing.cpu_count() - 1)
    p = multiprocessing.Pool(cpu_count)
    baseWeights = [1.0, 0.0, 0.0, 1.0]
    
    avgScore = 10000
    while avgScore > 30:
        allWeights = GenerateWeights(baseWeights)
        print ("Evaluating the following weights", allWeights)
        results = p.map(EvaluateWeights, allWeights)
        (baseWeights, avgScore) = findNewBase(results)
        print ("Average score of currentGeneration", avgScore)
        print ("New BaseWeights:", baseWeights)
        
        