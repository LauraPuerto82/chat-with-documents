import glob
import os


def scan_folders(directory="data"):
    """
    Recursively scans the specified directory and returns a list of all files.

    Args:
        directory (str): The directory to scan. Defaults to "data".

    Returns:
        list: A list of file paths found in the directory and its subdirectories.
    """
    files = [
        file
        for file in glob.glob(f"{directory}/**/*", recursive=True)
        if os.path.isfile(file)
    ]

    return files


if __name__ == "__main__":
    print(scan_folders())
