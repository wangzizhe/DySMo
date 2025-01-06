"""
Copyright (C) 2016 Alexandra Mehlhase
Copyright (C) 2025 Zizhe Wang

Original implementation by Alexandra Mehlhase and Amir Czwink.
Updated by Zizhe Wang.

This program is licensed under the GNU General Public License (GPL), version 3 or later.
See the LICENSE file or <http://www.gnu.org/licenses/> for details.
"""

# Libraries
import os
import sys
import PySimLib
# Local Imports
from Definitions import *
from exceptions.ModeException import ModeException
from Mode import Mode
from Plots import *
from Transition import Transition
from VSM import VSM

# Functions
def ExecPythonFile(fileName):
	"""
	Executes a Python file by dynamically reading, compiling, and executing its content.
	"""
	with open(fileName, 'r') as file:
		content = file.read()
	code = compile(content, fileName, 'exec')
	exec(code)
	
def Solver(name):
	"""
	Retrieves a solver instance by name using the PySimLib library.
	"""
	return PySimLib.FindSolver(name)
	
# Determine the default function to execute
func = VSM.simulate 
	
# Command-line argument checks
if len(sys.argv) == 1:
	print("Please provide a path to a variable-structure simulation description file as an argument.")
	print("Exiting...")
	exit()
	
if(len(sys.argv) == 3):
	if(sys.argv[2] == "clean"):
		func = VSM.clean
	else:
		print("You specified the following unknown argument:", sys.argv[2])
		print("Exiting...")
		exit()

# Resolve configuration path
configPath = os.path.abspath(sys.argv[1]);

# Instantiate the model
model = VSM(configPath)  # The global model instance

# Execute the configuration script
ExecPythonFile(sys.argv[1])

# Run the simulation
os.chdir(model.getPath())  # Switch to the model's directory
try:
	func(model)
except ModeException as e:
	print("ERROR:", e)
	print("See Log file for details.")
	
# Shutdown and cleanup
model.shutdown()
