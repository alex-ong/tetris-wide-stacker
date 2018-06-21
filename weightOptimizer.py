
import TetrisField
import LayoutCreator
import multiprocessing
from multiprocessing import cpu_count
import random
import itertools

from FieldEvaluator import PIECE_HEIGHT_SCORE, MAX_HEIGHT_SCORE, LINE_SCORE, BUMPINESS_SCORE, OTHER_PIECE_CONFORM_SCORE

PROGRESS_BAR = False
try:
    import tqdm
    PROGRESS_BAR = True
except:
    pass

def noFunc():
    pass


def scoreField(field):
    columnHeights = field.getColumnHeights()    
    score = min(columnHeights)  # score is how many completed lines there are.
    return score


def EvaluateWeights(weights):  
    total = 0  
    for _ in range(NUM_SIMULATIONS_PER_WEIGHTS):
        field = TetrisField.TetrisField(15, 30)
        layout = LayoutCreator.LayoutCreator(field, noFunc, weights)
        layout.createLayout()
        score = scoreField(field)
        total += score
    total = total / float(NUM_SIMULATIONS_PER_WEIGHTS)        
    return (weights, total)


def mutateIndex(weights, index):
    if index == PIECE_HEIGHT_SCORE:
        weights[index] += random.uniform(-0.03, 0.03)
    elif index == MAX_HEIGHT_SCORE:
        weights[index] += random.uniform(-0.03, 0.03)
    elif index == LINE_SCORE:
        weights[index] += random.uniform(-0.03, 0.03)
    elif index == BUMPINESS_SCORE:
        weights[index] += random.uniform(-0.03, 0.03)
    elif index == OTHER_PIECE_CONFORM_SCORE:
        weights[index] += random.uniform(-0.4, 0.4)

        
def getMutators(bestIndividuals):
    results = []
    for weights in bestIndividuals:
        for i in range(len(weights)):
            newResult = weights.copy()
            mutateIndex(newResult, i)
            results.append(newResult)
    return results


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
            if left[index] != weight:  # quick redundancy check.
                newResult = pair[0].copy()
                newResult[index] = weight
                results.append(newResult)
    return results


baseWeights = [0.8677493555073127, 0.97453014898381, 1.0178958787096912, 0.9315999576603519, 5.0] 
bestIndividualSize = 5    
iterations = 100
current_iteration = 0
NUM_SIMULATIONS_PER_WEIGHTS = 5            
if __name__ == '__main__':
    cpu_count = max(1, multiprocessing.cpu_count() - 1)
    pool = multiprocessing.Pool(cpu_count)
    global pbar
    # 1. Initialize Population
    allWeights = [baseWeights.copy(), baseWeights.copy()]  # population of 2.
     
    # 2. Evaluate population
    results = list(pool.imap_unordered(EvaluateWeights, allWeights))

    results.sort(key=lambda result: result[1], reverse=True)  
    # 3. while (!stopcondition) do:
    while current_iteration < iterations:        
        # 4. select best-fit individuals for reproduction        
        results = results[:bestIndividualSize]
            
        bestIndividuals = results[:]
        bestIndividuals = [item[0] for item in bestIndividuals]  # get weights only.
        
        # 5. breed new individuals through crossover and mutation
        # 5.1 breed via mutation.
        mutators = getMutators(bestIndividuals)        
        # 5.2 breed via crossover
        crossovers = getCrossover(bestIndividuals)         
        # 6. evaluate the individual fitness of new individuals
        childWeights = mutators + crossovers        

        poolTasks = pool.imap_unordered(EvaluateWeights, childWeights)
        if PROGRESS_BAR:
            childResults = list(tqdm.tqdm(poolTasks, total=len(childWeights)))
        else:
            childResults = list(poolTasks)
                        
        # 7. replace least-fit population with new individuals. 
        results += childResults
        results.sort(key=lambda result: result[1], reverse=True)
        current_iteration += 1
        printout = ("Iteration " + str(current_iteration) + str(results[0]))
        print (printout)
        with open ("optimization.txt", 'a') as f:
            f.write(printout)
        
