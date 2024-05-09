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
            mongo_data = {
                "ml_training_set" : games_statistics_dict,
                "teams_statistics": teams_statistics_dict
            }

            self.mongo_db_connector.insert_data(mongo_data)
        
        except Exception as e:
            ic("Exception!",e)