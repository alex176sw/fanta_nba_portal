import argparse
from trainer import TrainerService
import logging

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config-file", type=str, required=True)
    return parser.parse_args()

if __name__ == "__main__":
    logging.basicConfig(filename='inference.log', level=logging.INFO)
    logging.info("Starting Trainer Service")       
    trainer_service = TrainerService(cli())
    trainer_service.run()
