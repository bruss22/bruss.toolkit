#!/usr/bin/python3
from main import *
scope = int(input('Press 1 to generate traffic: '))
if scope == 1:
    print('Checking for urllist.csv')
    filestate = tkit.fileExists('urllist.csv')
    if filestate == False:
        print('urllist.csv not found')
    if filestate != False:
        with open ('urllist.csv') as csvfile:
            reader = csv.reader(csvfile,delimiter=",")
            data = list(reader)
        while True:
            try:
                url = random.choice(data)
                cache = tkit.urlList(url)
                print(f'Trying {url[0]} Result: {cache.status_code} {cache.reason}')
                time.sleep(1)
            except KeyboardInterrupt:
                print("Cancelled")
                break
            except AttributeError:
                time.sleep(.5)
                #cache = type(cache)
                print(f'error:{url[0]}-{cache} ' )