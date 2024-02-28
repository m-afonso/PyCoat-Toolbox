class Bath:

    def __init__(self,
                 bath_weight: int | float | None = None,
                 bath_nv: int | float = 0,
                 bath_pb: int | float = 0):

        if not isinstance(bath_weight, (int, float, type(None))):
            raise TypeError('Bath weight must be an integer or float.')

        if not isinstance(bath_nv, (int, float)):
            raise TypeError('Bath NV must be an integer or float.')
        elif not 0 <= bath_nv <= 1:
            raise ValueError('Bath NV must be between 0 and 1.')

        if not isinstance(bath_pb, (int, float)):
            raise TypeError('Bath PB must be an integer or float.')
        elif bath_pb < 0:
            raise ValueError('Bath PB must be non-negative.')

        if bath_weight is None:
            bath_weight = 0

        self.weight = float(bath_weight)
        self.pigment = float((bath_nv * bath_pb) / (1 + bath_pb))
        self.binder = bath_nv - self.pigment

    def __str__(self):
        return (f'W: {self.weight:.4f} | NV: {self.nv():.4f} | PB: {self.pb():.4f} | '
                f'P: {self.pigment:.4f} | B: {self.binder:.4f}')

    # def pigment(self):
    #     return self.__pigment * self.weight

    # def binder(self):
    #     return self.__binder * self.weight

    def pb(self):
        """
        Calculates the Pigmento to Binder (P/B) ratio.

        :return: float
        """

        if self.binder == 0:
            return .0

        return self.pigment / self.binder

    def nv(self):
        """
        Calculates the Non-Volatile ratio.
        :return: float
        """
        if self.weight == 0:
            return 0

        return self.pigment + self.binder

    def volatiles(self):
        return 1 - self.pigment - self.binder

    def remove_bath(self, new_bath_weight: int | float = 0):
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

        self.weight -= aliquot.weight

        return aliquot

    def add_bath(self, *other_bath):

        weight_accumulator = self.weight
        pigment_accumulator = self.weight * self.pigment
        binder_accumulator = self.weight * self.binder

        for bath in other_bath:
            weight_accumulator += bath.weight
            pigment_accumulator += bath.pigment * bath.weight
            binder_accumulator += bath.binder * bath.weight

        self.weight = weight_accumulator
        self.pigment = pigment_accumulator / weight_accumulator
        self.binder = binder_accumulator / weight_accumulator

        return None

    def add_pigment(self, amount_of_pigment: int | float):
        total_weight = self.weight + amount_of_pigment
        self.pigment = (amount_of_pigment + self.pigment * self.weight) / total_weight
        self.binder = (self.binder * self.weight) / total_weight
        self.weight = total_weight

        return self

    def add_binder(self, amount_of_binder: int | float):
        total_weight = self.weight + amount_of_binder
        self.binder = (amount_of_binder + self.binder * self.weight) / total_weight
        self.pigment = (self.pigment * self.weight) / total_weight
        self.weight = total_weight

        return self

    # def change_weight(self, new_weight):
    #     """
    #     Changes the weight of the bath.
    #
    #     Automatically adjusts pigment and binder.
    #     :param new_weight:
    #     """
    #     self.weight = new_weight


if __name__ == '__main__':
    bath = Bath(1000, 0.25, 0)
    print(bath)
    bath.add_binder(1000)
    print(bath)
