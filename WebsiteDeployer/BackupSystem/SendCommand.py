from ServerManager.Connection import Connection
import paramiko
import logging


def execute_command(conn: Connection, command: str):
    """
    Executes command on server side through SSH
    :param conn: Connection instance
    :param command: command to execute on server side
    :return: command output
    """
    try:

        logging.debug("Executing command: " + command)

        # Execute command
        stdin, stdout, stderr = conn.ssh_con.exec_command(command)

        # Get return code (exit code)
        command_return_code = int(stdout.channel.recv_exit_status())

        # Success (Return code zero)
        if command_return_code == 0:
            logging.debug("Command successfully executed with exit code 0.")
            # return output as string
            return stdout.read().decode()

        # Non zero return code or stderr present
        elif stderr.read().decode() or command_return_code != 0:
            logging.critical("Fatal error. Command execution error on server side (return code: "
                             + str(command_return_code) + ") "
                             + str(stderr.read().decode()))
            raise Exception("Fatal error. Command execution error on server side")

    except paramiko.ssh_exception.SSHException as sshe:
        raise Exception("Fatal error. Cannot execute command on server side: " + str(sshe))
