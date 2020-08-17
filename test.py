#!/usr/bin/env python3
import pandas as pd
import sys
sys.path.append('/home/hdr/PycharmProjects/meteo_parser/venv/lib/python3.5/site-packages')
print(sys.path)
df = pd.read_csv("2019-07-07-SN19011-measure.dat", delimiter=";", header=0, skiprows=[0, 2, 3], encoding="iso-8859-1")
print(df)