import os 
import json
from pathlib import Path

def CheckCache(file_path):

    dir_path = file_path.parent
    if os.path.exists(dir_path):
        if os.path.exists(file_path):
            return True  # cache exists
    else:
        os.mkdir(dir_path)
        return False

def CacheData(file_path, data):

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        return 1

def LoadCache(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        cache_data = json.load(file)
    return cache_data