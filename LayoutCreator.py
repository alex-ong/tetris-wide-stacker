'''
Class that does the main loop that creates a layout.
'''
import TetrisField, TetrisPiece, FieldEvaluator
from StallCounter import StallCounter


class ShuffleMarker(object):
    pass

STRICT = 0 # only allow maximum of 14 pieces of non placement
LENIENT = 1 # allow infinite as long as a piece can be placed
STALL_MODE=STRICT

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
        numPieces = int(self.field.width * self.field.height / 4)  # only fill 65%
        piecesPlaced = 0
        stallCounter = StallCounter()
        stallPieces = 0
        
        while piecesPlaced < numPieces:        
            piece = self.getPiece()            
            
            validPlacements = FieldEvaluator.listValidPlacements(self.field, piece)
            finalPlacements = FieldEvaluator.evaluate(self.field, validPlacements, self.weights)
            
            if len(finalPlacements) > 0:                
                self.field.placePiece(finalPlacements[0][1])  # choose first one for now
                self.onPlacePiece()
                piecesPlaced += 1
                if STALL_MODE == LENIENT:
                    stallCounter.resetStall()
                else:
                    stallPieces = 0   
            else:
                self.returnPiece(piece)
                if STALL_MODE == LENIENT:
                    stallCounter.addStall(piece.typeString)                                    
                    if stallCounter.isStalled():
                        break            
                else:
                    stallPieces += 1
                    if stallPieces > 14:
                        break
            
        return piecesPlaced          
    
                
def printField(field):
    print(field)
    print('\n')


if __name__ == '__main__':
    weights = [0.8890815185456057, 0.97453014898381, 1.0407397937520542, 0.9422826076414598, 5.0]
    field = TetrisField.TetrisField(45, 30)
    layout = LayoutCreator(field, lambda: printField(field), weights)
    layout.createLayout()
    print (layout.field)
    print ("Done")
    print (len(layout.nextPieces))
