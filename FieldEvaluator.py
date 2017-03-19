'''
Basic wrapper around Field that can be fed pieces to evaluate
'''

def evaluate(field, piece):
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
    results = evaluate(field, piece)
    for result in results:
        print (result)
