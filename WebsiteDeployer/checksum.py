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


    def get_local_files(self):
        files = []
        for root, _, filenames in os.walk(self.local_project_root):
            for filename in filenames:
                files.append(os.path.join(root, filename))

        return files

    def get_remote_files(self):
        out = execute_command(conn=self.conn, command=f"find {self.remote_project_root} -type f")
        return out.split()

