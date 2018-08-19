import os
import pandas as pd

from abc import abstractmethod, ABCMeta

from files import *


class SeriesBiuld(object, metaclass=ABCMeta):

    sources = {
        "ONS": ons.Ons,
        "ANA": ana.Ana
    }

    def __init__(self, data=None, path=os.getcwd(), source=None, *args, **kwargs):
        self.path = path
        if data is not None:
            self.data = data
        else:
            if source in self.sources:
                self.source = source
                self.data = self.sources[self.source](self.path, *args, **kwargs).data
            else:
                raise KeyError('Source not supported!')

        self.date_start = self.data.index[0]
        self.date_end = self.data.index[-1]

    @abstractmethod
    def month_start_year_hydrologic(self, station):
        pass

    @abstractmethod
    def plot_hydrogram(self):
        pass
    
    def __str__(self):
        """
        """
        return self.data.__repr__()
    
    def __getitem__(self, val):
        """
        """
        return self.__class__(data=self.data[val].copy(), source=self.source)

    def date(self, date_start=None, date_end=None):
        """
        """
        if date_start is not None and date_end is not None:
            date_start = pd.to_datetime(date_start, dayfirst=True)
            date_end = pd.to_datetime(date_end, dayfirst=True)
            return self.__class__(data = self.data.loc[date_start:date_end].copy())
        elif date_start is not None:
            date_start = pd.to_datetime(date_start, dayfirst=True)
            return self.__class__(data = self.data.loc[date_start:].copy())
        elif date_end is not None:
            date_end = pd.to_datetime(date_end, dayfirst=True)
            return self.__class__(data = self.data.loc[:date_end].copy())

    def flawless_period(self, station):
        """
        """
        aux = list()
        list_start = list()
        list_end = list()
        gantt_bool = self.data.isnull()[station]
        for i in gantt_bool.index:
            if ~gantt_bool.loc[i]:
                aux.append(i)
            elif len(aux) > 2 and gantt_bool.loc[i]:
                list_start.append(aux[0])
                list_end.append(aux[-1])
                aux = []
        if len(aux) > 0:
            list_start.append(aux[0])
            list_end.append(aux[-1])
        dic = {'Inicio': list_start, 'Fim': list_end}
        return pd.DataFrame(dic)

    def summary(self):
        """
        """
        return self.data.describe()

    def get_year(self, year):
        """
        Seleciona todos os dados referente ao ano. 
        """
        return self.__getitem__(year)

    def get_month(self, month):
        """
        Selecina todos os dados referente ao mês
        """
        return self.__class__(data=self.data.groupby(lambda x: x.month).get_group(month),
        source=self.source)
