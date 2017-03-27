'''
Basic wrapper around Field that can be fed pieces to listValidPlacements
'''
SUB_FIELD_COLUMNS = 8

def evaluate(field, validPlacements, weights):
    scoreTuples = []
    for validPlacement in validPlacements:
        score = evaluateSingle(field, validPlacement, weights)
        scoreTuples.append((score, validPlacement))
            
    scoreTuples.sort(key=lambda tup:tup[0])
    
    return scoreTuples

def clampRange(fieldWidth, x):
    '''
    given x, creates a subset of the field's width, SUB_FIELD_COLUMNS wide.
    Autoclamps and shifts things over near the borders
    '''
    startX = x - int(SUB_FIELD_COLUMNS / 2)
    endX = x + int(SUB_FIELD_COLUMNS / 2)
    lastFieldIndex = fieldWidth - 1
    if startX < 0:
        endX -= startX  # shift everything right
        startX = 0
    elif endX > lastFieldIndex:
        diff = lastFieldIndex - endX
        endX = lastFieldIndex
        startX -= diff
        
    return (startX, endX)    
    
def evaluateSingle(field, placement, weights):
    # do the placement.
    field.placePiece(placement)
    (startX, endX) = clampRange(field.width, placement.topLeftCorner[1]) 
    
    # do each test and add results
    columnHeights = field.getColumnHeights(startX, endX)
    
    pieceHeightScore = field.height - placement.topLeftCorner[0]
    maxColumnHeightScore = max(columnHeights)
    completedLineScore = min(columnHeights)
    bumpinessScore = evaluateBumpiness(columnHeights)
        
    field.unplacePiece(placement)
    # return sum of scores
    return (pieceHeightScore * weights[0] +
            maxColumnHeightScore * weights[1] +
            completedLineScore * weights[2] +
            bumpinessScore * weights[3]) 
    
def evaluateBumpiness(columnHeights):
    score = 0
    prevHeight = columnHeights[0]
    for i in range(1, len(columnHeights)):
        score += abs(prevHeight - columnHeights[i])**2 #square, so holes of size 4 are REALLY bad.
        prevHeight = columnHeights[i] 
    return score

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
