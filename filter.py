from abc import ABC, abstractmethod
from typing import List
from scipy import signal

class Filtration(ABC):
    """
    Абстрактный класс для определения общего интерфейса классов фильтрации.

    """

    @abstractmethod
    def create_filter(self, freq_sample_rate: float,
        frequency: List[float],
        order: int
        ) -> tuple:

        """
        Абстрактная функция для определения общего интерфейса функции фильтрации.

        Args:
            freq_sample_rate: Частота дискретизации сигнала.
            frequency: Список частот для фильтрации.
            order: Порядок фильтра.

        Returns:
            filter_parameters: Кортеж из двух массивов, представляющих коэффициенты фильтра.

        """

        pass


    def filter_data(self, trace: List[float],
        freq_sample_rate: float,
        frequency: List[float],
        order: int
        ) -> List[float]:
        """
        Функция для применения фильтра к данным.

        Args:
            trace: Список данных для фильтрации.
            freq_sample_rate: Частота дискретизации сигнала.
            frequency: Список частот для фильтрации.
            order: Порядок фильтра.

        Returns:
            filtered_trace: Список отфильтрованных данных.

        """
        b, a = self.create_filter(freq_sample_rate, frequency, order)
        return signal.filtfilt(b, a, trace)

class LowPassFiltration(Filtration):
    """
    Класс для низкочастотной фильтрации данных.

    """

    def create_filter(self, freq_sample_rate: float,
        frequency: List[float],
        order: int
        ) -> tuple:
        """Создает параметры фильтра нижних частот.

        Args:
            freq_sample_rate: Частота дискретизации сигнала.
            frequency: Список частот для фильтрации.
            order: Порядок фильтра.

        Returns:
            filter_parameters: Кортеж из двух массивов, представляющих коэффициенты фильтра.

        """
        low_freq = frequency[0]
        filter_parameters = signal.butter(order, low_freq, fs=freq_sample_rate, btype='low')
        return filter_parameters

class HighPassFiltration(Filtration):
    """
    Класс для высокочастотной фильтрации данных.

    """

    def create_filter(self, freq_sample_rate: float,
        frequency: List[float],
        order: int
        ) -> tuple:
        """Создает параметры фильтра высоких частот.

        Args:
            freq_sample_rate: Частота дискретизации сигнала.
            frequency: Список частот для фильтрации.
            order: Порядок фильтра.

        Returns:
            filter_parameters: Кортеж из двух массивов, представляющих коэффициенты фильтра.

        """
        high_freq = frequency[1]
        filter_parameters = signal.butter(order, high_freq, fs=freq_sample_rate, btype='high')
        return filter_parameters

class BandPassFiltration(Filtration):
    """
    Класс для полосовой фильтрации данных.

    """

    def create_filter(self, freq_sample_rate: float,
        frequency: List[float],
        order: int
        ) -> tuple:
        """Создает параметры полосового фильтра.

        Args:
            freq_sample_rate: Частота дискретизации сигнала.
            frequency: Список частот для фильтрации.
            order: Порядок фильтра.

        Returns:
            filter_parameters: Кортеж из двух массивов, представляющих коэффициенты фильтра.

        """
        filter_parameters = signal.butter(order, frequency, fs=freq_sample_rate, btype='band')
        return filter_parameters


