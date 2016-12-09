# still better than .ini files!
import yaml


def parse_config(config_file):
    with open(config_file) as f:
        return yaml.load(f)
