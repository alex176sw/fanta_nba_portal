from dg.providers.nba_api_impl import NbaApiDataProviderImpl

class NbaDataService:

    def __init__(self, nba_data_provider: NbaApiDataProviderImpl):

        self.nba_data_provider = nba_data_provider

    def get_played_games_of_current_season(self):

        return self.nba_data_provider.get_played_games_of_season("2023")