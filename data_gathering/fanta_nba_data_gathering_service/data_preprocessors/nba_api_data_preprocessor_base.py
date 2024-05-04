from abc import ABC, abstractmethod
class DataPreProcessorBase(ABC):

    @abstractmethod
    def get_dataset(self):
        pass
