'''
Simple array implementation of TetrisField.

Can check if a given tetrisPiece can fit.
'''

import TetrisPiece

from enum import Enum

class PerfectFit(Enum):
    PERFECT = 0
    EXIT = 1
    CONTINUE = 2

EMPTY = '.'
LIMIT = 'X'
class TetrisField(object):
    def __init__(self, width=0, height=0):
        self.data = [[EMPTY for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height
        
    def copy(self):
        result = TetrisField()  # create empty field       
        result.data = [row[:] for row in self.data]
        result.width = self.width  # post-set width/height
        result.height = self.height
        
        return result
    
    def findDrop(self, piece):
        # modifies the piece's position by only changing y value.
        # returns null if dropping it creates a gap. (e.g. s/z in neutral on the floor)
        currentResult = self.isPerfectFit(piece)
        while (currentResult == PerfectFit.CONTINUE):
            piece.topLeftCorner[0] += 1
            currentResult = self.isPerfectFit(piece)
        if currentResult == PerfectFit.EXIT:
            return None
        else:        
            return piece
    
    # returns if the current piece placement is happy
    def isPerfectFit(self, piece):        
        # first, check if we collide.
        finalPositions = []
        piecePosition = piece.topLeftCorner
                
        for offset in piece.currentOrientation:
            finalY = offset[0] + piece.topLeftCorner[0]
            finalX = offset[1] + piece.topLeftCorner[1]
            finalPositions.append((finalY, finalX))
        
        if self.collides(finalPositions):
            return PerfectFit.EXIT
        else:
            # place the piece then check under the piece to make sure it conforms perfectly
            self.placePiece(piece)
            allCellsHappy = True
            for position in finalPositions:
                positionBelow = (position[0] + 1, position[1])          
                positionLeft = (position[0], position[1] - 1)
                positionRight = (position[0], position[1] + 1)
                
                # place values of cells into variables...
                cellDown = self.getCellValue(positionBelow[0], positionBelow[1])
                cellLeft = self.getCellValue(positionLeft[0], positionLeft[1])
                cellRight = self.getCellValue(positionRight[0], positionRight[1]) 
                
                # (position, cellVal, cellCanBeEmpty)
                comparisons = ((positionBelow, cellDown, False), (positionLeft, cellLeft, True), (positionRight, cellRight, True))
                
                for comparison in comparisons:
                    (pos, cellVal, emptyOK) = comparison
                    if pos in finalPositions:  # ok
                        continue
                    elif cellVal == LIMIT:  # ok
                        continue
                    elif cellVal == piece.typeString:
                        allCellsHappy = False
                        break
                    elif (cellVal == EMPTY and not emptyOK):
                        allCellsHappy = False
                        break 

            self.unplacePiece(piece)
            if allCellsHappy:
                return PerfectFit.PERFECT
            else:
                return PerfectFit.CONTINUE
    
    # safe get cell value. returns LIMIT if outside bounds
    def getCellValue(self, y, x):
        try:
            result = self.data[y][x]
        except IndexError:
            result = LIMIT
        return result
    
    def cellHappy(self, typeString1, typeString2):
        return typeString1 != typeString2
            
    # returns true if any of the positions given collide with the matrix        
    def collides(self, positions):    
        for position in positions:
            (y, x) = position
            try:
                if self.data[y][x] != '.':
                    return True
            except IndexError:
                return True
                
        return False
    
    def placePiece(self, piece):
        (posOffsetY, posOffsetX) = piece.topLeftCorner
        for offset in piece.currentOrientation:
            (y, x) = offset
            self.data[y + posOffsetY][x + posOffsetX] = piece.typeString
            
    def unplacePiece(self, piece):
        (posOffsetY, posOffsetX) = piece.topLeftCorner
        for offset in piece.currentOrientation:
            (y, x) = offset
            self.data[y + posOffsetY][x + posOffsetX] = EMPTY  
              
    def __str__(self):
        resultRows = []        
        for row in self.data:
            resultRows.append(''.join(row))        
        return '\n'.join(resultRows)
        
        

if __name__ == '__main__':    
    x = 0
    fieldWidth = 16
    fieldHeight = 20
    field = TetrisField(fieldWidth, fieldHeight)
    fields = []
    
    # put each piece in each orientation in 4x4 empty grid things
    for piece in TetrisPiece.getBag():
        for i in range(len(piece.offsets)):
            piece.SetCurrentOrientation(i)
            for j in range(fieldWidth):
                piece.SetPosition(j, 0)
                result = field.findDrop(piece)
                if result is not None:
                    field.placePiece(result)
                    fields.append(field.copy())
                    field.unplacePiece(result)                    
    
    for field in fields:
        print(field , '\n')
    
