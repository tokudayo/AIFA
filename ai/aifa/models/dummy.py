import numpy as np

from aifa.base import HpeModel


class DummyHpeModel(HpeModel):
    def __init__(self):
        pass

    def forward(self, *args, **kwargs):
        return np.random.rand(18, 4)

    def postprocess(self, *args, **kwargs):
        return np.random.rand(18, 4)
