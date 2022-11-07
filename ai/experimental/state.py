

class StateSeries(object):
    '''
    Create a fixed length series of states
    '''
    def __init__(self, length: int = 5):
        self.data = ['static'] * length

    def __getitem__(self, slice):
        return self.data[slice]

    def update(self, state: str):
        self.data = self.data[1:] + [state]

    def latest_state(self):
        return self.data[-1]

    def max(self):
        return max(self.data,key=self.data.count)
    
    def min(self):
        return min(self.data,key=self.data.count)


