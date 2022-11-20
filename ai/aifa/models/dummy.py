import numpy as np

from aifa.base import HpeModel


class DummyHpeModel(HpeModel):
    def __init__(self):
        pass

    def forward(self, *args, **kwargs):
        return np.random.rand(17, 3)
