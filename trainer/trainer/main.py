import argparse
from trainer import TrainerService

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--mongo-config-file", type=str, required=True)
    return parser.parse_args()

if __name__ == "__main__":
    print("Starting Trainer Service")
    trainer_service = TrainerService(cli())
    trainer_service.run()
