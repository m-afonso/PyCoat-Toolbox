import numpy as np
from typing import *


class Bath:
    def __init__(self,
                 bath_weight: int | float,
                 bath_nv: int | float,
                 bath_pb: int | float):

        if not isinstance(bath_weight, (int, float)):
            raise TypeError('Bath weight must be an integer or float.')

        if not isinstance(bath_nv, (int, float)):
            raise TypeError('Bath NV must be an integer or float.')
        elif not 0 <= bath_nv <= 1:
            raise ValueError('Bath NV must be between 0 and 1.')

        if not isinstance(bath_pb, (int, float)):
            raise TypeError('Bath PB must be an integer or float.')
        elif bath_pb < 0:
            raise ValueError('Bath PB must be non-negative.')

        self.weight = float(bath_weight)
        self.pigment = float((bath_nv * bath_pb) / (1 + bath_pb)) * bath_weight
        self.binder = float(bath_nv * bath_weight - self.pigment)

    def pb(self):
        """
        Calculates the Pigmento t Binder (P/B) ratio.

        :return: float
        """
        return self.pigment / self.binder

    def nv(self):
        """
        Calculates the Non-Volatile ratio.
        :return: float
        """

        return (self.pigment + self.binder) / self.weight

    def remove_bath(self,
                    new_bath_weight: int | float = 0):
        """
        Removes an aliquot of the bath.
        :param new_bath_weight:
        :return:
        """

        if new_bath_weight < 0:
            raise ValueError('Bath PB must be non-negative.')
        elif new_bath_weight > self.weight :
            raise ValueError('Aliquot weight cannot be greater than the bath weight.')

        self.weight -= float(new_bath_weight)

        return Bath(new_bath_weight, bath_nv=self.nv(), bath_pb=self.pb())

    def add_bath(self,
                 other_bath: Type[Bath]):

        self.weight += other_bath.weight
        self.pigment += other_bath.pigment
        self.binder += other_bath.binder
