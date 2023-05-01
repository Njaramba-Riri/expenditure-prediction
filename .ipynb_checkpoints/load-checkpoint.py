import os
import pandas as pd

DATASET_PATH=os.path.join('Datasets')


def fetch_data(path=DATASET_PATH):
    if not os.path.isdir(path):
        os.makedirs(path)
    for filename in ("train.csv", "test.csv"):
        filepath = os.path.join(path, filename)
        if not os.path.isfile(filepath):
            print(f" '{filename}' doesn't exist.")
            urllib.request.urlretrieve(url + filename, filepath)        


def load_data(filename):
    fetch_data()
    file=os.path.join(path, filename)
    return(file, error_bad_lines=False)
    
    
 