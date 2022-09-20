import numpy as np

from .base import HpeModel


class DummyHpeModel(HpeModel):
    def __init__(self):
        pass

    def forward(self, image):
        return np.random.rand(18, 2)