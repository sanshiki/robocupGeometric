import json


class ConfigLoader:
    def __init__(self, param_file):
        self.param_file = param_file
        self.params = self.load_json(param_file)

    def load_json(self, file):
        with open(file, 'r') as f:
            return json.load(f)