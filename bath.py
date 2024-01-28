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

    def __str__(self):
        return f'Weight: {self.weight}, NV: {self.nv():.2f}, PB: {self.pb():.2f}'

    def pb(self):
        """
        Calculates the Pigmento t Binder (P/B) ratio.

        :return: float
        """

        if self.binder == 0:
            return 0

        return self.pigment / self.binder

    def nv(self):
        """
        Calculates the Non-Volatile ratio.
        :return: float
        """
        if self.weight == 0:
            return 0

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
        elif new_bath_weight > self.weight:
            raise ValueError('Aliquot weight cannot be greater than the bath weight.')

        aliquot = Bath(new_bath_weight, bath_nv=self.nv(), bath_pb=self.pb())

        self.pigment -= aliquot.pigment
        self.binder -= aliquot.binder
        self.weight -= aliquot.weight

        return aliquot

    def add_bath(self,
                 *other_bath):

        for bath in other_bath:
            self.weight += bath.weight
            self.pigment += bath.pigment
            self.binder += bath.binder
