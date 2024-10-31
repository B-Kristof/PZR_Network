import sys


def prompt_skip_backup():
    print("WARNING: Backup was not created due to an exception. "
                      "This means that ALL of the current files will be OVERWRITTEN and you have no up to date backup.")
    if input("Do you want to continue? (y or n)") == "n":
        sys.exit()