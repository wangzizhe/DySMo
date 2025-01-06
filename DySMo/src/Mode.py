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
import PySimLib
import time

class Mode:
	"""
	Represents a simulation mode in the DySMo framework.
	Encapsulates settings, tools, and transitions for a specific mode of a variable-structure model.
	"""

	def __init__(self):
		"""
		Initializes a new Mode instance with default values.
		"""
		# Private members
		self.__vsmModel = None
		self.__id = None
		self.__mdlObj = None  # PySimLib model object
		self.__lastSimNum = None
		self.__simObjs = {}  # Dictionary of simulation objects for this mode
		
		# Public members
		self.files = []
		self.modeRef = None  # Mode reference identifier
		self.solver = None  # Solver settings
		self.synonym = {}  # Synonym mappings
		self.tool = None  # PySimLib tool for simulationm
		self.transitions = []  # Outgoing transitions
		
	def __str__(self):
		return f"Mode {self.__id}"
		
	def compile(self):
		"""
		Compiles the mode by preparing its PySimLib model object.
		"""
		print(f"Compiling mode {self.get_id()}...")
		self.tool.Compile(self.__mdlObj)
		
	def find_transition(self):
		"""
		Finds the outgoing transition based on the 'transitionId' end value.
		"""
		transId = int(self.get_endValue("transitionId"))
		if(transId > len(self.transitions)):
			from exceptions.InvalidTransitionException import InvalidTransitionException;
			raise InvalidTransitionException(self, transId)
		return self.transitions[transId-1]
		
	def get_endValue(self, varName):
		return self.__mdlObj.variables[varName].final
		
	def get_id(self):
		return self.__id
		
	def get_model(self):
		return self.__vsmModel
		
	def get_parameter(self, key):
		return self.__mdlObj.parameters[key]
		
	def has_endValue(self, varName):
		return varName in self.__mdlObj.variables
		
	def init(self, model, modeId):
		"""
		Initializes the mode by setting up its model, tools, and transitions.
		"""
		from exceptions.InvalidModeModelException import InvalidModeModelException
		
		self.__vsmModel = model
		self.__id = modeId
		
		# Use the default solver if not specified
		if self.solver is None:
			self.solver = model.default_solver
			
		# Acquire PySimLib model object
		if self.modeRef is None:
			raise InvalidModeModelException(self)
			
		self.__mdlObj = PySimLib.Model(self.modeRef, self.files)
		if self.__mdlObj is None :
			raise InvalidModeModelException(self)
			
		# Set directories on the model object
		self.__mdlObj.outputName = f'm{self.get_id()}'
		base_path = model.getPath()
		self.__mdlObj.outputDir = os.path.join(base_path, "output")
		self.__mdlObj.resultDir = os.path.join(base_path, "result")
		self.__mdlObj.simDir = base_path
		# Select the simulation tool
		self.tool = self._select_tool()
			
		# Initialize transitions
		for transId, transition in enumerate(self.transitions, start=1):
			transition.init(transId)
	
	def _select_tool(self):
		"""
		Selects a compatible simulation tool for the mode.
		"""
		if self.tool is not None:
			tool = PySimLib.FindTool(self.tool)
			if tool is not None:
				return tool
			print(f"Desired tool for mode {self.__id} is not available.")
		
		# Try the default tool
		if self.__vsmModel.default_tool and self.__vsmModel.default_tool.Accepts(self.__mdlObj):
			return self.__vsmModel.default_tool

		# Fall back to a compatible tool
		compatible_tools = self.__mdlObj.GetCompatibleTools()
		if compatible_tools:
			print(f"Choosing tool '{compatible_tools[0]}' for mode {self.__id}.")
			return compatible_tools[0]

		print(f"No simulator is available for mode {self.__id}. Exiting...")
		exit(1)

	def read_init(self):
		"""
    	Reads and initializes the simulation model for this mode.
    	Ensures the critical variable 'transitionId' is present in the model.
		"""
		from exceptions.MissingTransitionIdException import MissingTransitionIdException
		
		# Initialize the model using the selected tool
		self.tool.ReadInit(self.__mdlObj)
		
		# Validate that 'transitionId' exists in the model's variables
		if 'transitionId' not in self.__mdlObj.variables:
			raise MissingTransitionIdException(self)
		
	def read_last_result(self):
		return self.read_result(self.__lastSimNum)
		
	def read_result(self, simNum):
		return self.tool.ReadResult(self.__simObjs[simNum])
		
	def set_initialValue(self, varName, value):
		self.__mdlObj.variables[varName].start = value
		
	def set_parameter(self, name, value):
		self.__mdlObj.parameters[name] = value
		
	def set_parameters(self, params):
		for key, value in params.items():
			self.set_parameter(key, value)
		
	def simulate(self):
		"""
		Simulates the mode and logs the results.
		"""
		simObj = PySimLib.Simulation(self.__mdlObj, self.__vsmModel.getCurrentSimulationNumber())
		
		simObj.startTime = self.__vsmModel.currentTime
		simObj.stopTime = self.__vsmModel.stopTime
		if self.solver is not None:
			simObj.solver = self.solver
		
		print(f"Running simulation {simObj.GetSimNumber()} - ModeID: {self.get_id()} - Time: {self.__vsmModel.currentTime}")
		t1 = time.perf_counter()
		self.tool.Simulate(simObj)
		t2 = time.perf_counter()
		
		elapsed_time = t2 - t1
		print(f"Simulation {simObj.GetSimNumber()} completed in {elapsed_time:.2f} seconds.")
		PySimLib.Log.Line(f"Simulation {simObj.GetSimNumber()} of mode {self.get_id()} took {elapsed_time:.2f} seconds.")
		
		self.__lastSimNum = simObj.GetSimNumber()
		self.__simObjs[self.__lastSimNum] = simObj
		return elapsed_time
		
	def write_init(self, inits):
		"""
		Sets the initial values for multiple variables in the model.
		"""
		for varName, value in inits.items():
			self.__mdlObj.variables[varName].start = value