from fanta_nba_data_gathering_service.providers.nba_data_provider import NbaDataProviderBase

from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import teams

class NbaApiDataProviderImpl(NbaDataProviderBase):
    
    def get_played_games_of_season(self, season_start_year: str):

        assert len(season_start_year) == 4
        next_year = int(season_start_year[-2:])+1
        season_year = f"{season_start_year}-{next_year}"

        gamefinder = leaguegamefinder.LeagueGameFinder(
            season_nullable=season_year
        )

        games = gamefinder.get_data_frames()[0]
        
        return games
