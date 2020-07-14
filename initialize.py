#Title: Initialization file for DUHI
#Date: 13-07-2020
#Author: Harro Jongen
#Sets correct working directory for DUHI

import os
import inspect

#Set source file location as working directory
module_path = inspect.getfile(inspect.currentframe())
module_dir = os.path.realpath(os.path.dirname(module_path))
os.chdir(module_dir)


