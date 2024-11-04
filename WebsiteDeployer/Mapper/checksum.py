import hashlib
import logging
import os
from Models import SSHServerConnection
from ServerManager.SendCommand import execute_command


class ChecksumMapper:
    def __init__(self, conn: SSHServerConnection, local_project_root: str, remote_project_root: str):
        self.conn = conn
        self.local_project_root = local_project_root
        self.remote_project_root = remote_project_root
        self.local_files_and_checksums = self.get_local_files()
        self.remote_files_and_checksums = self.get_remote_files()
        self.generate_local_checksums()
        self.generate_remote_checksums()
        logging.debug("Checksums generated.")

    @classmethod
    def check_if_folder_blacklisted(cls, file_path, folder_blacklist: list):
        for b_folder in folder_blacklist:
            if b_folder in file_path.split("\\") or b_folder in file_path.split("/"):
                return True

        return False

    def get_local_files(self):
        folder_blacklist = [
            ".git",
            "__pycache__",
            ".idea"
        ]
        files = []
        for root, _, filenames in os.walk(self.local_project_root):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                if not self.check_if_folder_blacklisted(full_path, folder_blacklist):
                    element = {
                        "relative_file_path": os.path.normpath(full_path.removeprefix(self.local_project_root)),
                        "file": full_path,
                        "checksum": ""
                    }
                    files.append(element)

        return files

    def get_remote_files(self):
        folder_blacklist = [
            ".git",
            "__pycache__",
            ".idea"
        ]
        files = []

        out = execute_command(conn=self.conn, command=f"find {self.remote_project_root} -type f")
        for filename in out.splitlines():
            if not self.check_if_folder_blacklisted(filename, folder_blacklist):
                element = {
                    "relative_file_path": os.path.normpath(filename.removeprefix(self.remote_project_root)),
                    "file": filename,
                    "checksum": ""
                    }
                files.append(element)
        return files

    @classmethod
    def generate_local_checksum(cls, file_path: str):
        try:
            md5_hash = hashlib.md5()
            with open(file_path, "rb") as file:
                while True:
                    data = file.read(65536)  # Read the file in 64K chunks
                    if not data:
                        break
                    md5_hash.update(data)

            return md5_hash.hexdigest()
        except Exception as e:
            logging.warning(f"Cannot calculate local checksum for {file_path}: {str(e)}")
            return ""

    def generate_remote_checksum(self, file_path: str):
        try:
            # Check if md5sum installed on remote server
            res = execute_command(conn=self.conn, command='md5sum "' + file_path + '"', mute_logs=True)
            return res.split()[0]

        except Exception as e:
            logging.warning(f"Cannot calculate remote checksum for {file_path}: {str(e)}")
            return ""

    def generate_local_checksums(self):
        logging.info("Generating MD5 checksums locally...")
        for i, element in enumerate(self.local_files_and_checksums):
            self.local_files_and_checksums[i]["checksum"] = self.generate_local_checksum(self.local_files_and_checksums[i]["file"])

    def generate_remote_checksums(self):
        logging.info("Generating MD5 checksums on remote server...")
        for i, element in enumerate(self.remote_files_and_checksums):
            self.remote_files_and_checksums[i]["checksum"] = self.generate_remote_checksum(
                self.remote_files_and_checksums[i]["file"]
            )

    def delta_calculator(self):
        logging.info("Calculating deltas...")
        local_set = {(file["relative_file_path"], file["checksum"]) for file in self.local_files_and_checksums}
        remote_set = {(file["relative_file_path"], file["checksum"]) for file in self.remote_files_and_checksums}
        delta = local_set - remote_set
        return [file for file in self.local_files_and_checksums if
                (file["relative_file_path"], file["checksum"]) in delta]
