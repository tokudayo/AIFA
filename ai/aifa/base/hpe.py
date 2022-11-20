class HpeModel(object):
    def __init__(self):
        '''
        Define model initialization.
        '''
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        return self.predict(*args, **kwargs)

    def predict(self, *args, **kwargs):
        '''
        Predict method.
        '''
        results = self.forward(*args, **kwargs)
        return results

    def forward(self):
        '''
        Forward method. Should handle a single image or a batch of images.
        '''
        raise NotImplementedError
