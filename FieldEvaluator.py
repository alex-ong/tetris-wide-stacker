'''
Basic wrapper around Field that can be fed pieces to listValidPlacements
'''

def evaluate(field, validPlacements):
    scoreTuples = []
    for validPlacement in validPlacements:
        score = evaluate_single(field, validPlacement)
        scoreTuples.append((score, validPlacement))
            
    scoreTuples.sort(key=lambda tup:tup[0])
    
    return scoreTuples

def evaluate_single(field, placement):
    # do the placement.
    
    # do each test and add results    
    score = -placement.topLeftCorner[0]  # stub for now
    
    # return sum of scores
    return score

# todo
def evaluate_completed_lines(field, xRange):
    pass
def evaluate_bumpiness(field, xRange):
    pass

def listValidPlacements(field, piece):
    results = []        
    for i in range(len(piece.offsets)):
        results.extend(generateOrientation(field, piece, i))        
    return results
    
def generateOrientation(field, piece, orientationIndex):
    results = []
    piece.SetCurrentOrientation(orientationIndex)
    for x in range(field.width):        
        result = generatePosition(field, piece, x)
        if result is not None:
            results.append(result)
    return results
    
def generatePosition(field, piece, x):
    piece.SetPosition(x, 0)
    result = field.findDrop(piece)
    if result is not None:
        return piece.copy()
    return None


if __name__ == '__main__':
    import TetrisField, TetrisPiece
    field = TetrisField.TetrisField(20, 8)
    piece = TetrisPiece.IPiece()
    results = listValidPlacements(field, piece)
    finalPlacement = evaluate(results)
    field.placePiece(finalPlacement)
    print(field)
