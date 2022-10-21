class StallCounter(object):
    def __init__(self):
        self.values = {}
        for key in "LOSTJIZ":
            self.values[key] = False

    def isStalled(self):
        for value in self.values.values():
            if not value:
                return False
        return True

    def resetStall(self):
        for key in self.values.keys():
            self.values[key] = False

    def addStall(self, letter):
        self.values[letter] = True
