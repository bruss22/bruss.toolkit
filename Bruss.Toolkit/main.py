#!/usr/bin/python3
import urllib3
import requests
import random
import time
from os.path import exists
import csv
class tkit:
    def urlList(url):
        urllib3.disable_warnings()
        try:
            #first line is for DPI with cert referenced in folder used by FGT for DPI
            #response = requests.get(url[0], verify='/home/fortinet/toolkit/FGTSPI.cer',timeout=12)
            response = requests.get(url[0], verify=False,timeout=6)
            #print(f'Trying - {row[0]}: Result - {response.status_code}')
            return response
        except requests.exceptions.ReadTimeout:
            return (f'Trying - {url[0]}: Result - Timeout')
        except Exception as exception:
            return exception          
    def fileExists(filename):
        filestate = exists(f'{filename}')
        return exists