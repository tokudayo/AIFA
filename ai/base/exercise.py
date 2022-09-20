class Exercise(object):
    def __init__(self):
        '''
        Initialization. Should include a name and a reference time series for comparison?
        '''
        raise NotImplementedError

    def rule(self):
        '''
        Evaluation rule of the exercise.
        '''
        raise NotImplementedError
    

    def judge(self, candidate, *args, **kwargs):
        '''
        Jugde the performance of a time series.
        '''
        return self.compare(candidate, *args, **kwargs)

    def compare(self):
        '''
        Compare the actual time series with the reference time series.
        '''
        raise NotImplementedError