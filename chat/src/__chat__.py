from .chat import DataExplorerCrew
from typing import Dict
import yaml
import os

def test(inputs: Dict = {}) -> str:
    if len(inputs) == 0:
        # Load default inputs from a YAML file if no inputs are provided
        yaml_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'default_inputs.yaml')
        with open(yaml_file, 'r') as file:
            inputs = yaml.safe_load(file)
    # Run the crew with the provided inputs
    result = DataExplorerCrew().crew().kickoff(inputs=inputs)
    return result.raw

if __name__ == "__main__":
    test()