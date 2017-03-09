from pathlib import Path


def folder(path):
    destination = Path(path)
    destination.mkdir(exist_ok=True, parents=True)
    return destination
