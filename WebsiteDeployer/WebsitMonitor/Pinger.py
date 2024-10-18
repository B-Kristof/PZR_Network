import requests


def ping_target(target: str):
    return requests.get(target).status_code == 200