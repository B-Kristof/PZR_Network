import logging
import os
from Models import SSHServerConnection
from ServerManager.SendCommand import execute_command
import xxhash

class CheckSumChecker:
    def __init__(self, conn: SSHServerConnection, local_project_root: str, remote_project_root: str):
        self.conn = conn
        self.local_project_root = local_project_root
        self.remote_project_root = remote_project_root
        self.local_files_and_checksums = self.get_local_files()
        self.remote_files_and_checksums = self.get_remote_files()


    def get_local_files(self):
        files = []
        for root, _, filenames in os.walk(self.local_project_root):
            for filename in filenames:
                element = {
                    "file": filename,
                    "checksum": ""
                }
                files.append(element)

        return files

    def get_remote_files(self):
        files = []
        out = execute_command(conn=self.conn, command=f"find {self.remote_project_root} -type f")
        for filename in out.split():
            element = {
                "file": filename,
                "checksum": ""
                }
            files.append(element)
        return out.split()

    @classmethod
    def generate_local_checksum(cls, file_path: str):
        hash_xxhash = xxhash.xxh64()  # You can use xxh32 or xxh128 as well, depending on your needs

        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):  # Read in chunks to handle large files
                hash_xxhash.update(chunk)

        return hash_xxhash.hexdigest()

    def generate_remote_checksum(self, file_path: str):
        return execute_command(self.conn, "xxhsum -H3 /path/to/your/file | awk '{print $1}'")

    def generate_local_checksums(self):
        for element in self.local_files_and_checksums:
            element["checksum"] = self.generate_local_checksum(element["file"])

    def generate_remote_checksums(self):
        for element in self.remote_files_and_checksums:
            element["checksum"] = self.generate_remote_checksum(element["file"])