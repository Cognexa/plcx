import logging
import ruamel.yaml

from typing import Any


logger = logging.getLogger(__name__)


def load_yaml(path: str) -> Any:
    """
    Load yaml file or object with ruamel.yaml.

    :param path: path to file
    :return: return yaml object
    """
    try:
        with open(path, 'r') as file:
            return ruamel.yaml.load(file, ruamel.yaml.RoundTripLoader)
    except ruamel.yaml.YAMLError as error:
        raise TypeError(f'Yaml file `{path}` has invalid format. `{error.args}`')
