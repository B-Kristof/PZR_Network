import logging
from ErrorHandler.FatalErrorHandler import FatalError


# NOT WORKING
def extension_filter_files(file_list: list, extension_blacklist: list):
    for file in file_list:
        for extension in extension_blacklist:
            if file["relative_file_path"].endswith(extension):
                file_list.remove(file)

    return file_list

# NOT WORKING
def folder_filter_files(file_list: list, folder_blacklist: list):
    for file in file_list:
        for folder in folder_blacklist:
            if folder in file["file"]:
                file_list.remove(file)

    return file_list


def filter_files(file_list: list, extension_blacklist: list, folder_blacklist: list):
    try:
        logging.debug("Filtering deployment files...")
        return folder_filter_files(extension_filter_files(file_list, extension_blacklist), folder_blacklist)
    except Exception as e:
        fatal_handler = FatalError(e, "Cannot filter files due to a fatal error.")
        fatal_handler.display_error()
