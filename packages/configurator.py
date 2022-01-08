import json


class Configurator:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.read_config()

    def read_config(self):
        with open(self.config_file, 'r') as f:
            config = json.load(f)
            f.close()
        return config

    def get_config(self):
        return self.config

    def write_config(self, config):
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
            f.close()