"""
download_data.py
----------------
Downloads the MovieLens Small Dataset from GroupLens and extracts
movies.csv and ratings.csv into the data/ folder.

Run this once before launching the app:
    python data/download_data.py
"""

import os
import zipfile
import urllib.request
import shutil

DATASET_URL = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_PATH = os.path.join(DATA_DIR, "ml-latest-small.zip")
EXTRACT_DIR = os.path.join(DATA_DIR, "ml-latest-small")


def download_dataset():
    print("Downloading MovieLens Small Dataset...")
    try:
        urllib.request.urlretrieve(DATASET_URL, ZIP_PATH)
        print(f"Downloaded to: {ZIP_PATH}")
    except Exception as e:
        print(f"Download failed: {e}")
        print("Please manually download from:")
        print("  https://grouplens.org/datasets/movielens/latest/")
        print(f"and place movies.csv and ratings.csv in: {DATA_DIR}")
        return False
    return True


def extract_dataset():
    print("Extracting files...")
    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        z.extractall(DATA_DIR)

    # Move movies.csv and ratings.csv up to data/
    for filename in ["movies.csv", "ratings.csv"]:
        src = os.path.join(EXTRACT_DIR, filename)
        dst = os.path.join(DATA_DIR, filename)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"Extracted: {filename}")

    # Clean up zip and extracted folder
    os.remove(ZIP_PATH)
    if os.path.exists(EXTRACT_DIR):
        shutil.rmtree(EXTRACT_DIR)
    print("Cleanup complete.")


def main():
    movies_path = os.path.join(DATA_DIR, "movies.csv")
    ratings_path = os.path.join(DATA_DIR, "ratings.csv")

    if os.path.exists(movies_path) and os.path.exists(ratings_path):
        print("Dataset already present. No download needed.")
        return

    if download_dataset():
        extract_dataset()
        print("\nDataset ready!")
    else:
        print("\nFailed to download dataset automatically.")


if __name__ == "__main__":
    main()
