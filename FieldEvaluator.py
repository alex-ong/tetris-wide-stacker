'''
Basic wrapper around Field that can be fed pieces to listValidPlacements
'''

def evaluate(validPlacements):    
    maxPlacement = None
    for placement in validPlacements:
        if maxPlacement is None:
            maxPlacement = placement
        elif placement.topLeftCorner[0] > maxPlacement.topLeftCorner[0]:
            maxPlacement = placement

    return maxPlacement

def listValidPlacements(field, piece):
    results = []        
    for i in range(len(piece.offsets)):
        results.extend(evaluateOrientation(field, piece, i))        
    return results
    
def evaluateOrientation(field, piece, orientationIndex):
    results = []
    piece.SetCurrentOrientation(orientationIndex)
    for x in range(field.width):        
        result = evaluatePosition(field, piece, x)
        if result is not None:
            results.append(result)
    return results
    
def evaluatePosition(field, piece, x):
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
