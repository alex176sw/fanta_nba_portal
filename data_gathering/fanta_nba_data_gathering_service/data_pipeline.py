from icecream import ic

class DataPipeline:

    def __init__(self, mongo_db_connector, nba_data_service, nba_data_preprocessor):
        self.mongo_db_connector = mongo_db_connector
        self.nba_data_service = nba_data_service
        self.nba_data_preprocessor = nba_data_preprocessor
            
    def update_mongo_database_with_latest_data(self):
        
        try:
            ic("Downloading data..")
            games_df = self.nba_data_service.get_played_games_of_current_season()
            ic("Preprocessing data..")
            games_statistics_dict, teams_statistics_dict = self.nba_data_preprocessor.get_statistics(games_df)
            ic("Sending data to MongoDB..")
            games_data = {
                "games_statistics" : games_statistics_dict,
            }
            teams_data = {
                "teams_statistics": teams_statistics_dict
            }

            self.mongo_db_connector.insert_data_into_games_collection(games_data)
            self.mongo_db_connector.insert_data_into_teams_stats_collection(teams_data)

        except Exception as e:
            ic("Exception!",e)