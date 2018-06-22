class StallCounter(object):
    def __init__(self):
        self.L = False
        self.O = False
        self.S = False
        self.T = False
        self.J = False
        self.I = False
        self.Z = False
    
    def isStalled(self):
        return (self.L and self.O and self.S and self.T 
                and self.J and self.I and self.J)
    
    def resetStall(self):
        self.L = False
        self.O = False
        self.S = False
        self.T = False
        self.J = False
        self.I = False
        self.Z = False
        
    def addStall(self, letter):
        if letter == 'L':
            self.L = True
        elif letter == 'O':
            self.O = True
        elif letter == 'S':
            self.S = True
        elif letter == 'T':
            self.T = True
        elif letter == 'J':
            self.J = True
        elif letter == 'I':
            self.I = True
        elif letter == 'Z':
            self.Z = True
