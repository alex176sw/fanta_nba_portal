import argparse

from icecream import ic

from fanta_nba_data_gathering_service.data_pipeline import DataPipeline
from fanta_nba_data_gathering_service.data_preprocessors.nba_api_data_preprocessor import NbaApiDataPreProcessor
from fanta_nba_data_gathering_service.mongo_db_connector import MongoDBConnector
from fanta_nba_data_gathering_service.nba_data_service import NbaDataService
from fanta_nba_data_gathering_service.providers.nba_api_impl import NbaApiDataProviderImpl
from fanta_nba_data_gathering_service.task_scheduler import TaskScheduler


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--mongo-config-file", type=str, required=True)
    return parser.parse_args()

def main(args):

    ic("Application started!")

    dp = DataPipeline(
        MongoDBConnector(config_file=args.mongo_config_file),
        NbaDataService(NbaApiDataProviderImpl()),
        NbaApiDataPreProcessor()
    )

    scheduler = TaskScheduler()
    h="08:00"
    scheduler.schedule_daily_job(
        h, dp.update_mongo_database_with_latest_data
    )
    scheduler.run_all()
    ic(f"Application will run at {h} each day!")
    scheduler.run_scheduler()


if __name__=='__main__':
    args = cli()
    main(args)