import logging
import json
import os
from src.ErrorHandler import FatalErrorHandler
from src.Models.Config import Config

class ConfigLoader:
    def __init__(self, config_files: list, classes_parse_to: list):
        self.config_files = config_files
        self.classes_parse_to = classes_parse_to

    def load_configs(self) -> Config:
        try:
            instances = {}

            subclasses = ConfigLoader.__subclasses__()
            if len(self.classes_parse_to) != len(self.config_files):
                logging.error("Number of subclasses must match the number of config files and classes.")
                raise Exception("Fatal error: cannot load configurations!")

            for i, subclass in enumerate(subclasses):
                if i < len(self.config_files):
                    subloader = subclass(self.config_files[i], self.classes_parse_to[i])
                    res = subloader.load_config()
                    instances[self.classes_parse_to[i].__name__] = res  # Direct assignment instead of using update()
                    logging.debug(f"{self.classes_parse_to[i].__name__} configuration loaded.")

            # Create config object
            config = Config()
            for key in instances.keys():
                setattr(config, key.lower(), instances[key])  # Use lower() to maintain consistency

            return config
        except ValueError as ve:
            fatal_handler = FatalErrorHandler.FatalError(ve, "Fatal Value Error while loading and parsing configuration files.")
            fatal_handler.display_error()
        except Exception as e:
            fatal_handler = FatalErrorHandler.FatalError(e, "Fatal Error while loading and parsing configuration files.")
            fatal_handler.display_error()

class WebserverConfigLoader(ConfigLoader):
    def __init__(self, file_path: str, class_to_parse):
        super().__init__([file_path], [class_to_parse])  # Pass the file_path and class_to_parse
        self.file_path = file_path
        self.class_to_parse = class_to_parse

    def load_config(self):
        try:
            logging.debug("Loading webserver information...")
            json_data = load_json(self.file_path)
            if json_data is False:
                logging.error(f"Failed to load JSON from {self.file_path}.")
                raise
            servers = []
            for key in list(json_data.keys()):
                servers.append(parse_to_instance(json_data[key], self.class_to_parse))
            logging.debug(f"Webserver configuration loaded.")
            return servers

        except FileNotFoundError as fnf:
            FatalErrorHandler.FatalError(fnf, f"{self.file_path} file not found").display_error()
        except Exception as e:
            FatalErrorHandler.FatalError(e, f"Fatal error while loading {self.file_path} file").display_error()


class ProgramConfigLoader(ConfigLoader):
    def __init__(self, file_path: str, class_to_parse):
        super().__init__([file_path], [class_to_parse])  # Pass the file_path and class_to_parse
        self.file_path = file_path
        self.class_to_parse = class_to_parse

    def load_program_config(self):
        try:
            json_data = load_json(self.file_path)
            if json_data is False:
                logging.error(f"Failed to load JSON from {self.file_path}.")
                raise
            instance = parse_to_instance(json_data, self.class_to_parse)
            return instance
        except FileNotFoundError as fnf:
            FatalErrorHandler.FatalError(fnf, f"{self.file_path} file not found").display_error()
        except Exception as e:
            FatalErrorHandler.FatalError(e, f"Fatal error while loading {self.file_path} file").display_error()


def load_json(infile_path: str) -> dict | bool:  # Changed to 'dict | bool'
    """
    :param infile_path: path and json file
    :return: dict or False if failed
    """
    if not os.path.exists(infile_path):
        return False

    try:
        with open(infile_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        logging.error(f"Error loading JSON from {infile_path}: {str(e)}")
        return False


def parse_to_instance(json_data: dict, obj_class):
    try:
        # Get the attributes (parameters) from the __init__ method of the class
        attributes = obj_class.__init__.__annotations__.keys() if hasattr(obj_class.__init__, '__annotations__') else []

        # Filter json_data to include only relevant keys that match the class attributes
        filtered_data = {key: json_data[key] for key in attributes if key in json_data}

        # Create an instance of the class with the filtered data
        instance = obj_class(**filtered_data)

        # Load remaining json data as instance properties
        for key, value in json_data.items():
            if not hasattr(instance, key):
                setattr(instance, key, value)

        return instance

    except Exception as e:
        logging.critical(f"Fatal error. Cannot create {obj_class.__name__} instance: {str(e)}")
        raise Exception("Cannot create config loader class instance!")
