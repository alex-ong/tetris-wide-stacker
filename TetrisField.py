'''
Simple array implementation of TetrisField.

Can check if a given tetrisPiece can fit.
'''

import TetrisPiece

class TetrisField(object):
    def __init__(self, width=0, height=0):
        self.data = [['.' for _ in range(width)] for _ in range(height)]
        
    def copy(self):
        result = TetrisField()        
        result.data = [row[:] for row in self.data]
        return result
    
    def placePiece(self, piece):
        (posOffsetY, posOffsetX) = piece.topLeftCorner
        for offset in piece.currentOrientation:
            (y, x) = offset
            self.data[y + posOffsetY][x + posOffsetX] = piece.typeString
            
            
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
            piece.SetPosition(int(x % fieldWidth), int(x / fieldWidth) * 4)
            field.placePiece(piece)
            x += 4
        fields.append(field.copy())  # testing out copy function.
    
    for field in fields:
        print(field , '\n')
    
