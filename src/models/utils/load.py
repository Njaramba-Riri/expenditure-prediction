import urllib.request
from rich import print

import os
import pandas as pd

PROJECT_DIR = "."
DATASET_PATH = os.path.join(PROJECT_DIR, 'Datasets')   
                
def fetch_data(path=DATASET_PATH):
    """Fetches data to used in 

    Args:
        path (_type_, optional): _description_. Defaults to DATASET_PATH.
    """
    #print(f"Path: {path}")
    if path is None:
        print("Provide a valid path.")
    if not os.path.isdir(path):
        print("Path doesn't exist, creating one...")
        os.makedirs(path)
    for filename in ("Train.csv", "Test.csv", "Train (1).csv", "Test (1).csv", "all.csv"):
        filepath = os.path.join(path, filename)
        if not os.path.isfile(filepath):
            print(f"{ filename } doesn't exist.")
    return path

def load_data(filename: str):
    data = fetch_data()
    file = os.path.join(data, filename)
    frame = pd.read_csv(file)
    return frame
    
    
 