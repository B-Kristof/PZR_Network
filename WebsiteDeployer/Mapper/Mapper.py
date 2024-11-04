from .checksum import ChecksumMapper
from ErrorHandler.FatalErrorHandler import FatalError
from .FileFilter import filter_files


def map_and_filter_files(webserver):
    try:
        checksum = ChecksumMapper(
            conn=webserver.conn,
            local_project_root=webserver.local_folder,
            remote_project_root=webserver.webserver_folder)

        delta_files = checksum.delta_calculator()

        print(webserver.specific_extensions_blacklist)
        print(webserver.specific_folders_blacklist)
        filtered_files = filter_files(
            file_list=delta_files,
            extension_blacklist=webserver.specific_extensions_blacklist,
            folder_blacklist=webserver.specific_folders_blacklist
        )

        webserver.deployment_files = filtered_files

    except Exception as e:
        fatal_handler = FatalError(e, "Cannot map files due to a fatal error.")
        fatal_handler.display_error()
