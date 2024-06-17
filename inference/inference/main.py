import argparse
from inference import InferenceService

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--mongo-config-file", type=str, required=True)
    return parser.parse_args()

if __name__ == "__main__":
    inference_service = InferenceService(cli())
    inference_service.run()