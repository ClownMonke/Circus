from itertools import cycle


class FreqList:
    __freq_cycle = cycle([1e3])


    def __init__(self, freq_array):
        self.__freq_cycle = cycle(freq_array)


    def get_next_freq(self):
        return next(self.__freq_cycle)
