from abc import ABC, abstractmethod

class NbaDataProviderBase(ABC):
    
    @abstractmethod
    def get_played_games_of_season(self):
        pass