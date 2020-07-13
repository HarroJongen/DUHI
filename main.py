#Title: Main file for DUHI
#Date: 16-06-2020
#Author: Harro Jongen
#Excecutes the complete proces to analyze the connections of drought and UHI for NL and BE

#Import packages
import os
import inspect
import datetime
import pandas as pd


#Set source file location as working directory
module_path = inspect.getfile(inspect.currentframe())
module_dir = os.path.realpath(os.path.dirname(module_path))
os.chdir(module_dir)

#Import functions
from Functions import SICFormatter
from Functions import WOWFormatter
from Functions import UrbanRuralCombiner
#from Functions import UrbanRuralFormatter

#Select period and format Amsterdata from Summer in the City to project's format
#SICFormatter.SICFormatter(start = datetime.datetime(2017, 1, 1), end = datetime.datetime(2018 , 12, 31), file = "Data/5G0D2194(5G0D2194)-1554817879612.xlsx")

#Format WOW-NL data
WOWFormatter.WOWFormatter('Amsterdam', start = datetime.datetime(2017, 1, 1),\
                          end = datetime.datetime(2018 , 12, 31), file = "Data/export_916696001.csv")
    

#Create csv with rural and urban station combinations
UrbanRuralCombiner.UrbanRuralCombiner()

#

