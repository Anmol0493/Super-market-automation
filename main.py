from pricesmart import *
from loshusansupermarket import *
import sys
import traceback
import os

config = []
filenames = ""
web = []

with open('userconfig.txt', 'r') as file:
    for line in file:
        line = line.replace('\n', '')
        if line != "":
            config.append(line)
            web=line.split('-')[0]
            filenames += str(line)
        
inputpath = "./input/"

dir_list = [str(x) for x in os.listdir(inputpath) if x.endswith('.csv') and x not in filenames]

for con in config:
    try:
        web = con.split('-')[0]
        f = con.split('-')[2]
        if not os.path.exists("./input/" + f):
            print("\033[91m File exists in the input directory but not in the userconfig, filename :- " + str(f) + "\033[0m")
            continue
        if web == 'PriceSmart':
            # print(web)
            process_config(con)
        elif web == 'Loshusan':
            # print(web)
            AddtoCart(con)
    except Exception as e:
        print("\033[91m "+str(e) + "\033[0m")
        print(sys.exc_info())
        print(traceback.format_exc())

input("Script Completed")
