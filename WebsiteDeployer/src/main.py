import ctypes
import logging
import os
import shutil
import sys

from src.BackupSystem.Compressor import compress_local_folder
from src.ConfigLoader.SetLogger import LogSetter
from src.ConfigLoader.ConfigLoader import ProgramConfigLoader, WebserverConfigLoader
from src.Models.ProgramConfig import ProgramConfig
from src.Models.Webserver import Webserver
from src.ErrorHandler import CleanUpHandler

# Set paramiko logging level to WARNING
logging.getLogger("paramiko").setLevel(logging.WARNING)


def main():
    webservers = []
    try:
        config_loader = ProgramConfigLoader("src/Data/config/deployer.json", ProgramConfig)
        program_config = config_loader.load_program_config()

        log_setter = LogSetter(level=program_config.logging_level)
        log_setter.setup_logging()

        # Load Webserver Configuration
        webserver_config_loader = WebserverConfigLoader("src/Data/config/webservers.json", Webserver)
        webservers = webserver_config_loader.load_config()

        if webservers:

            # Initialize Webserver
            for server in webservers:
                server.initialize()

        else:
            logging.debug("Could not find any loaded webserver.")
            logging.debug("Please check your configuration file.")

        # collect folders
        folders_to_deploy = []
        for folder in webservers[0].to_deploy:
            folders_to_deploy.append(webservers[0].local_folder + "\\" + folder)

            # compress folders to destination folder
            compress_local_folder(webservers[0].local_folder + "\\" + folder, "Compressed/") \
                if (os.path.isdir(webservers[0].local_folder + "\\" + folder)) \
                else shutil.copy2(webservers[0].local_folder + "\\" + folder, "Compressed/")

        # webservers[0].put_folder(webservers[0].local_folder, webservers[0].webserver_folder)


    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise
    finally:
        CleanUpHandler.cleanup(webservers)

if __name__ == "__main__":
    main()

