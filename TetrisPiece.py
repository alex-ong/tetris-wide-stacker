'''
Tetris piece is just a wrapper for an array. 
No real logic required since the Board will handle that.

Our arrays will be from topLeft to bottom right indexing

(0,0)(0,1) (0,2)
(1,0)(1,1) (1,2)
(2,0)(2,1) (2,2)

'''

# We will define our offsets arrays globally
# That way we can save heaps of memory when we construct thousands of temp pieces

O_NEUTRAL = ((0, 0), (0, 1), (1, 0), (1, 1))

I_NEUTRAL = ((0, 0), (0, 1), (0, 2), (0, 3))
I_VERT = ((0, 0), (1, 0), (2, 0), (3, 0))

T_NEUTRAL = ((0, 1), (1, 0), (1, 1), (1, 2))
T_REVERSE = ((1, 1), (0, 0), (0, 1), (0, 2))
T_LEFT = ((1, 0), (0, 1), (1, 1), (2, 1))
T_RIGHT = ((1, 1), (0, 0), (1, 0), (2, 0))

Z_NEUTRAL = ((0, 0), (0, 1), (1, 1), (1, 2))
Z_VERT = ((0, 1), (1, 0), (1, 1), (2, 0))

S_NEUTRAL = ((0, 1), (0, 2), (1, 0), (1, 1))
S_VERT = ((0, 0), (1, 0), (1, 1), (2, 1))

J_NEUTRAL = ((0, 0), (1, 0), (1, 1), (1, 2))
J_REVERSE = ((1, 2), (0, 0), (0, 1), (0, 2))
J_LEFT = ((2, 0), (0, 1), (1, 1), (2, 1))
J_RIGHT = ((0, 1), (0, 0), (1, 0), (2, 0))

L_NEUTRAL = ((0, 2), (1, 0), (1, 1), (1, 2))
L_REVERSE = ((1, 0), (0, 0), (0, 1), (0, 2))
L_LEFT = ((0, 0), (0, 1), (1, 1), (2, 1))
L_RIGHT = ((0, 0), (1, 0), (2, 0), (2, 1))

O_OFFSETS = (O_NEUTRAL,)
I_OFFSETS = (I_NEUTRAL, I_VERT)
T_OFFSETS = (T_NEUTRAL, T_REVERSE, T_LEFT, T_RIGHT)
Z_OFFSETS = (Z_NEUTRAL, Z_VERT)
S_OFFSETS = (S_NEUTRAL, S_VERT)
J_OFFSETS = (J_NEUTRAL, J_REVERSE, J_LEFT, J_RIGHT)
L_OFFSETS = (L_NEUTRAL, L_REVERSE, L_LEFT, L_RIGHT)

def getBag():
    pieces = (OPiece(), IPiece(), TPiece(), SPiece(), ZPiece(), JPiece(), LPiece())
    return pieces

class TetrisPiece(object):
    def __init__(self, offsets, typeString):
        self.offsets = offsets  # array of offset arrays, stored in (y,x) format
        self.typeString = typeString
        self.topLeftCorner = [0, 0]  # stored in y, x
        self.currentOrientation = None
        
    def SetPosition(self, x, y):
        self.topLeftCorner = [y, x]
        
    def SetCurrentOrientation(self, index):
        self.currentOrientation = self.offsets[index]
        
    def copy(self):
        result = TetrisPiece(self.offsets,self.typeString)
        result.topLeftCorner = self.topLeftCorner
        result.currentOrientation = self.currentOrientation
        return result
        
class OPiece(TetrisPiece):
    def __init__(self):
        super().__init__(O_OFFSETS, 'O')

class IPiece(TetrisPiece):
    def __init__(self):
        super().__init__(I_OFFSETS, 'I')
class TPiece(TetrisPiece):
    def __init__(self):
        super().__init__(T_OFFSETS, 'T')
class SPiece(TetrisPiece):
    def __init__(self):
        super().__init__(S_OFFSETS, 'S')
class ZPiece(TetrisPiece):
    def __init__(self):
        super().__init__(Z_OFFSETS, 'Z')
class JPiece(TetrisPiece):
    def __init__(self):
        super().__init__(J_OFFSETS, 'J')
class LPiece(TetrisPiece):
    def __init__(self):
        super().__init__(L_OFFSETS, 'L')
        
def prettyPrintPiece(offsetArray, typeString):    
    array = [[' ' for _ in range(4)] for _ in range(4)]    
    for offset in offsetArray:
        (y, x) = offset
        array[y][x] = typeString
    
    for row in array:
        print(row)
        
if __name__ == '__main__':
    pieces = getBag()
    for piece in pieces:
        for offset in piece.offsets:
            prettyPrintPiece(offset, piece.typeString)
            print ("\n") 
