import argparse
import logging
from inference import InferenceService

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config-file", type=str, required=True)
    return parser.parse_args()

if __name__ == "__main__":
    logging.basicConfig(filename='inference.log', level=logging.INFO)
    logging.info("Starting Inference Service")    
    inference_service = InferenceService(cli())
    inference_service.run()