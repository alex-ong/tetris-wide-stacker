'''
Class that does the main loop that creates a layout.
'''
import TetrisField, TetrisPiece, FieldEvaluator

class ShuffleMarker(object):
    pass

class LayoutCreator(object):
    def __init__(self, field, onPlacePiece, weights):
        self.field = field
        self.onPlacePiece = onPlacePiece
        self.nextPieces = []
        self.weights = weights
        self.refillBag()
    
    def getPiece(self):        
        result = self.nextPieces.pop(0)
        
        while isinstance(result, ShuffleMarker):  # fix for endless loop
            self.refillBag()
            result = self.nextPieces.pop(0)
        
        return result
    
    def returnPiece(self, piece):
        self.nextPieces.append(piece)
                
    def refillBag(self):
        self.nextPieces.extend(TetrisPiece.getRandomBag())
        self.nextPieces.append(ShuffleMarker())
        
    def createLayout(self):        
        numPieces = int(self.field.width * self.field.height / 4 / 2)  # only fill half high
        piecesPlaced = 0
        stallCounter = 0
        while piecesPlaced < numPieces:        
            piece = self.getPiece()            
            
            validPlacements = FieldEvaluator.listValidPlacements(self.field, piece)
            finalPlacements = FieldEvaluator.evaluate(self.field, validPlacements, self.weights)
            
            if len(finalPlacements) > 0:                
                self.field.placePiece(finalPlacements[0][1])  # choose first one for now
                self.onPlacePiece()
                piecesPlaced += 1
                stallCounter = 0    
            elif stallCounter < 14:  # no placements, put the piece back into end of queue                
                self.returnPiece(piece)
                stallCounter += 1
            else: #we have skipped 14 pieces. We must be stuck.
                break
            
        return piecesPlaced           


def printField(field):
    pass
    
if __name__ == '__main__':
    weights = [-0.05,0.0,0.0,1.0]
    field = TetrisField.TetrisField(150, 15)
    layout = LayoutCreator(field, lambda: printField(field), weights)
    layout.createLayout()
    print (layout.field)
