import argparse

from dg.data_pipeline import DataPipeline
from dg.data_preprocessors.nba_api_data_preprocessor import NbaApiDataPreProcessor
from dg.mongo_db_connector import MongoDBConnector
from dg.nba_data_service import NbaDataService
from dg.providers.nba_api_impl import NbaApiDataProviderImpl
from dg.task_scheduler import TaskScheduler


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--mongo-config-file", type=str, required=True)
    return parser.parse_args()

def main(args):

    dp = DataPipeline(
        MongoDBConnector(config_file=args.mongo_config_file),
        NbaDataService(NbaApiDataProviderImpl()),
        NbaApiDataPreProcessor()
    )

    scheduler = TaskScheduler()
    scheduler.schedule_daily_job(
        "21:38", dp.update_mongo_database_with_latest_data
    )
    scheduler.run_scheduler()
    #scheduler.run_all()


if __name__=='__main__':
    args = cli()
    main(args)