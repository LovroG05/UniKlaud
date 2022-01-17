import json
import os
from packages.MessageUtil import printWarning


class Configurator:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.read_config()

    def read_config(self):
        if os.path.isfile(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                f.close()
        else:
            printWarning("Config file not found, creating default config")
            config = {
                    "mountedStorageObjects": [],
                    "mainDriveName": "",
                }
            with open(self.config_file, "w") as f:
                json.dump(config, f)
                f.close()
        
        return config

    def get_config(self):
        return self.config

    def write_config(self, config):
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
            f.close()