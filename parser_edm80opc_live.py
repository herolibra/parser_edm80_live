#!/usr/bin/env python3

import sys
# sys.path.append('/home/hdr/PycharmProjects/meteo_parser/venv/lib/python3.5/site-packages')
# print(sys.path)
import os, re, json
from bs4 import BeautifulSoup
import requests
# import wget
import pandas as pd
from datetime import date, timedelta
import sync as sync
import copy
import datetime
import errno

import getopt


def printusage():
    """ Prints the usage message to STDOUT """
    print("Usage:", sys.argv[0], '[-v] -f <input data file>  -s <server>')


def printhelp():
    """ Prints the help message to STDOUT """
    print(__doc__.format())


def main(argv):
    """ Main routine. Parses arguments, reads CSV file, builds according FROST observations, and pushes them to the Server """

    furl = "http://193.196.38.108:8080/FROST-Server/v1.0/"

    try:
        opts, args = getopt.getopt(argv, "hvSf:s:", ["help", "verbose", "simulate", "file=", "server="])
    except getopt.GetoptError as err:
        print("Error:", err)
        printusage()
        sys.exit(errno.EINVAL)
    for opt, arg in opts:
        if opt in ["-h", "--help"]:
            printhelp()
            sys.exit()
        elif opt in ("-v", "--verbose"):
            opt_verbose = True
        elif opt in ("-S", "--simulate"):
            opt_simulate = True
        elif opt in ("-f", "--file"):
            inputfile = arg
        elif opt in ("-s", "--server"):
            furl = arg

    # if (inputfile == ""):
    #     printusage()
    #     sys.exit(errno.EINVAL)

    df = pd.read_csv(inputfile, delimiter=";", header=0, skiprows=[0, 2, 3], encoding="iso-8859-1")
    svtime = df.iloc[0]['date&time [UTC]']
    svtime = datetime.datetime.strptime(svtime, '%Y-%m-%d %H:%M:%S')

    sid_thing = 'saqn:t:teco.edu:crowdsensor:' + df.iloc[0]['serial-no']
    print(sid_thing)

    software_version = {svtime.strftime('%Y-%m-%d') + "Z": df.iloc[0]['software-version']}
    print(software_version)
    lon = df.iloc[0][35][1:].replace(",", ".")
    lat = df.iloc[0][36][1:].replace(",", ".")
    hei = df.iloc[0][37][1:].replace(",", ".")
    
    sync.thing(furl, sid_thing, 'things', lon, lat, hei)
    sensor_id = 'saqn:s:grimm-aerosol.com:EDM80OPC:SN-' + str(df.iloc[0]['serial-OPC'])
    sid_ds_base = 'saqn:ds:' + str(sid_thing[7:]) + '::' + sensor_id[7:]  # hardware derial.nr?

    sid_ds_pm10 = sid_ds_base + ":mcpm10"
    sid_ds_pm2p5 = sid_ds_base + ":mcpm2p5"
    sid_ds_pm1 = sid_ds_base + ":mcpm1"
    sid_ds_bins = sid_ds_base + ":bins"

    sync.datastream(furl, sid_thing, sid_ds_pm10, 'edm80opc', 'ds_pm10', sensor_id, software_version)
    sync.datastream(furl, sid_thing, sid_ds_pm2p5, 'edm80opc', 'ds_pm25', sensor_id, software_version)
    sync.datastream(furl, sid_thing, sid_ds_pm1, 'edm80opc', 'ds_pm1', sensor_id, software_version)
    sync.datastream(furl, sid_thing, sid_ds_bins, 'edm80opc', 'ds_bins', sensor_id, software_version)

    for label, content in df.iterrows():
        try:
            stime = content['date&time [UTC]']

            try:
                time = datetime.datetime.strptime(stime, '%Y-%m-%d %H:%M:%S')
            except:
                print("time error")
                continue

            ptime = time.strftime('%Y-%m-%dT%H:%M:%S') + "Z"
            l_cali = datetime.datetime.strptime(content['last calibration [local time]'], '%Y-%m-%d %H:%M:%S')
            l_cali_utc = l_cali.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'

            Bins = {}
            Bins['0,35 µm'] = content['0,35 [um]']
            Bins['0,46 µm'] = content['0,46 [um]']
            Bins['0,66 µm'] = content['0,66 [um]']
            Bins['1,00 µm'] = content['1,0 [um]']
            Bins['1,30 µm'] = content['1,3 [um]']
            Bins['1,70 µm'] = content['1,7 [um]']
            Bins['2,30 µm'] = content['2,3 [um]']
            Bins['3,00 µm'] = content['3,0 [um]']
            Bins['4,00 µm'] = content['4,0 [um]']
            Bins['5,20 µm'] = content['5,2 [um]']
            Bins['6,50 µm'] = content['6,5 [um]']
            Bins['8,00 µm'] = content['8,0 [um]']
            Bins['10,00 µm'] = content['10 [um]']
            Bins['12,00 µm'] = content['12 [um]']
            Bins['14,00 µm'] = content['14 [um]']
            Bins['16,00 µm'] = content['16 [um]']
            Bins['18,00 µm'] = content['18 [um]']
            Bins['20,00 µm'] = content['20 [um]']
            Bins['22,00 µm'] = content['22 [um]']
            Bins['25,00 µm'] = content['25 [um]']
            Bins['28,00 µm'] = content['28 [um]']
            Bins['31,00 µm'] = content['31 [um]']
            Bins['34,00 µm'] = content['34 [um]']
            Bins['37,00 µm'] = content['37 [um]']

            pm10 = float(content.iloc[3].replace(",", "."))
            pm2p5 = float(content.iloc[4].replace(",", "."))
            pm1 = float(content.iloc[5].replace(",", "."))

            # PM10
            sync.postObservation(furl, pm10, ptime, ptime, sid_ds_pm10, l_cali_utc)
            ##########################################
            # PM2p5
            sync.postObservation(furl, pm2p5, ptime, ptime, sid_ds_pm2p5, l_cali_utc)
            ##########################################
            # PM1
            sync.postObservation(furl, pm1, ptime, ptime, sid_ds_pm1, l_cali_utc)
            ##########################################

            # BINS
            sync.postObservation(furl, Bins, ptime, ptime, sid_ds_bins, l_cali_utc)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    main(sys.argv[1:])
