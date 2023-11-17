#!/home/rbatistavilela/miniconda3/envs/geoweather/bin/python3 -W ignore
# -*- coding: utf-8 -*-


'''
    File name: service.py
    Python Version: 3.6.0
'''

__author__ = "Ricardo Vilela"
__version__ = "0.1"
__email__ = ""
__status__ = "Development"

# Tag das Mensagens:
# [I] -> Informacao
# [A] -> Aviso/Alerta
# [E] -> Erro

import argparse
import sys
from datetime import datetime
import json

from controller import run_process

parser = argparse.ArgumentParser(description='''MRMS products decoder''',
                                 formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-v", "--verbose",  action='store_true', 
                                        dest='verbose', 
                                        help="Verbose", 
                                        default=False)

parser.add_argument("-c", "--configuration",type=str, 
                                        dest='config', 
                                        help="Initialization settings. ", 
                                        default=None,
                                        required=True)


parser.add_argument("-f", "--filename",type=str, 
                                        dest='filename', 
                                        help="raster filename", 
                                        default=None,
                                        required=False)

parser.add_argument("-filetime", "--filetime",  type=str, 
                                                dest='filetime', 
                                                help="File time to check for raster file YYYYmmddHHMM", 
                                                default=None,
                                                required=False)





args = parser.parse_args()

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("Start - {} ({}).".format(now, sys.argv[0]))
if __name__ == "__main__":
    
    config = json.loads(open(args.config, mode='r').read())
    filename = args.filename   
    filetime = datetime.strptime(args.filetime,'%Y%m%d%H%M')   
    
    run_process(filename=filename, filetime=filetime, config=config)

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("End - {} ({}).".format(now, sys.argv[0]))
