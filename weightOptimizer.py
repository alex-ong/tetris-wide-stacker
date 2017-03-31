
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
    score = -min(columnHeights) #score is how many completed lines there are.
    return score

def EvaluateWeights(weights):
    field = TetrisField.TetrisField(15, 30)
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
    for _ in range(20):
        result.append(baseWeights.copy())
    
    #make 5 mutations. Test them 5 times each.
    for _ in range(5):
        randomWeights =randomizeWeights(baseWeights)
        for __ in range(5):                         
            result.append(randomWeights)
    return result

def findNewBase(results):
    '''results are in the form (weights,score)'''
    # first concatenate results.
    
    newResults = {}
    
    for result in results:
        (weight, score) = result
        weight = tuple(weight)
        if weight in newResults:
            (totalScore, count) = newResults[weight]
            totalScore += score
            count += 1
            newResults[weight] = (totalScore, count) 
        else:
            newResults[weight] = (score, 1)
    
    results.clear()
    for key in newResults.keys():
        results.append((key, newResults[key][0]/newResults[key][1]))

    results.sort(key=lambda tup: tup[1])  # we want lowest score.
    print ("Finding new base out of", results)
    # average the first 5
    avgScore = 0.0
    finalResult = list(results[0][0])
    for i in range(1, 3):
        (result, score) = results[i]
        for j in range(len(finalResult)):
            finalResult[j] += result[j]
        avgScore += score
            
    for j in range(len(finalResult)):
        finalResult[j] /= 3.0
    avgScore /= 3
    
    
    return (finalResult, avgScore)
            
if __name__ == '__main__':
    cpu_count = max(1, multiprocessing.cpu_count() - 1)
    p = multiprocessing.Pool(cpu_count)
    baseWeights = [0.8677493555073127, 0.97453014898381, 1.0178958787096912, 0.9315999576603519, 5.0]
    
    avgScore = 10000
    retryCount = 0  # quit if we are unable to get a better optimization 5 times in a row.
    while avgScore > -25 :  # quit once we are sufficiently flat
        allWeights = GenerateWeights(baseWeights)        
        results = p.map(EvaluateWeights, allWeights)
        (newBaseWeights, newAvgScore) = findNewBase(results)
        if (newAvgScore < avgScore):
            avgScore = newAvgScore
            baseWeights = newBaseWeights
            retryCount = 0
        else:
            retryCount += 1
        print ("Average score of currentGeneration", avgScore)
        print ("New BaseWeights:", baseWeights)
        if retryCount > 5:
            break
        
        
