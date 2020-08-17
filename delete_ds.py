import numpy as np
import pandas as pd
import requests, json
from datetime import datetime

url = 'http://193.196.38.108:8080/FROST-Server/v1.0'
p = requests.delete(url + "/Observations")
if (p.status_code  == 201):
    print("Del successful")
else:
    print("Error:", p.status_code)
    for chunk in p.iter_content(chunk_size=128):
        print(chunk)
