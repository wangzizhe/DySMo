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
import pylab
import PySimLib
import shutil
import time

class VSM:
	"""
	Variable Structure Model (VSM) simulation framework.
	Handles the initialization, simulation, and management of modes, transitions, and results.
	"""

	def __init__(self, configPath):
		"""
		Initializes the VSM object with a configuration path.
		"""
		# Private members
		self.__path = os.path.abspath(os.path.join(configPath, os.pardir))
		self.__logPath = configPath + ".log"
		self.__logFile = open(self.__logPath, "w")
		self.__actMode = None  # Current mode
		self.__compiledModes = {}
		self.__currentNum = 1  # Simulation counter
		self.__observer = {}
		
		# Public members
		self.currentTime = 0
		self.default_solver = None
		self.default_tool = None
		self.init = {}
		self.modes = []
		self.observe = []
		self.plots = []
		self.startTime = 0
		self.stopTime = 1
		self.translate = True
		
		# Initialize log file
		PySimLib.Log.SetTarget(self.__logFile)
	
	# Private methods    
	def __compileMode(self, mode):
		"""
		Compiles a given mode if it has not been compiled yet.
		"""
		if mode not in self.__compiledModes:
			if self.translate:
				t1 = time.perf_counter()
				mode.compile()
				PySimLib.Log.Line(f"Compilation of mode {mode.get_id()} took {time.perf_counter() - t1:.2f} seconds.")
			self.__compiledModes[mode] = True
			mode.read_init()
		
	def __deleteFileSafe(self, folder):
		if os.path.exists(folder):
			os.remove(folder)
		
	def __deleteFolderSafe(self, folder):
		if os.path.exists(folder):
			shutil.rmtree(folder)
		
	def __drawPlots(self):
		show = False
		for p in self.plots:
			figure = pylab.figure()  # Create a new plot
			for var in self.observe:
				for i in range(len(self.__observer[var])):
					col = p.getColor(self.__observer["modeID"][i], i, var)
					if col is not None and self.__observer[var][i]:
						pylab.plot(self.__observer[p.xAxisVar][i], self.__observer[var][i], p.colorToColorString(col))
			pylab.grid(p.drawGrid)
			pylab.xlabel(p.labelXAxis)
			pylab.ylabel(p.labelYAxis)
			if hasattr(p, 'fileName'):
				pylab.savefig(os.path.join(self.__path, "result", p.fileName))
			if not hasattr(p, 'fileName') or hasattr(p, 'show'):
				show = True
			else:
				pylab.close(figure)
		if show:
			pylab.show()

	def __getOutputPath(self):
		return os.path.join(self.__path, "output")
		
	def __getResultPath(self):
		return os.path.join(self.__path, "result")
		
	def __init(self):
		"""
		Initializes the VSM observer and default tool.
		"""
		for k in self.observe:
			self.__observer[k] = []
		self.__observer["time"] = []
		self.__observer["modeID"] = []
		
		if self.default_tool:
			name = self.default_tool
			self.default_tool = PySimLib.FindTool(name)
			if self.default_tool is None:
				print(f"The specified default tool '{name}' is not available.")
		
	def __observe(self, simResults):
		"""
		Updates observer data based on simulation results.
		"""
		for k in self.observe:
			synonym = self.__actMode.synonym.get(k) if k in self.__actMode.synonym else k if k in simResults else None
			self.__observer[k].append(simResults.get(synonym, []))
		self.__observer["time"].append(simResults["time"])
		self.__observer["modeID"].append(self.__actMode.get_id())

	def __prepareFolders(self):
		resultPath = self.__getResultPath()
		self.__deleteFolderSafe(resultPath)
		time.sleep(1)
		os.makedirs(resultPath)
		
		outputPath = self.__getOutputPath()
		if not os.path.exists(outputPath):
			os.makedirs(outputPath)
		
	def __preprocess(self):
		"""
		Prepares modes for simulation and initializes the first mode.
		"""
		from exceptions.NoModeException import NoModeException
		if not self.modes:
			raise NoModeException()
		
		for modeId, mode in enumerate(self.modes, start=1):
			mode.init(self, modeId)
		
		self.__actMode = self.modes[0]
		self.__compileMode(self.__actMode)
		self.__actMode.write_init(self.init)
		
	def __save_observer(self):
		"""
		Saves observer data in both .mat and .csv formats.
		"""
		from PySimLib.Mat.Mat import Mat
		from PySimLib.Mat.OutputStream import OutputStream
		
		nan = float("NaN")
		variables = ["time", "modeID"] + self.observe
		mat = Mat()
		
		# Create the names matrix
		names = mat.AddTextMatrix("names", len(variables))
		for i, key in enumerate(variables):
			names.SetString(i, key)
		
		# Calculate the total number of data points
		nDataPointsPerSim = [
			max(len(self.__observer[key][i]) if isinstance(self.__observer[key][i], list) else 1 for key in variables)
			for i in range(len(self.__observer["modeID"]))
		]
		nDataPointsSum = sum(nDataPointsPerSim)
		
		# Create the values matrix with the correct size
		values = mat.AddMatrix("values", len(variables), nDataPointsSum)
		
		# Fill the values matrix
		col_offset = 0
		for sim_index, n_points in enumerate(nDataPointsPerSim):
			for var_index, key in enumerate(variables):
				data = self.__observer[key][sim_index]
				if key == "modeID":
					# modeID is a single value for each simulation
					for col in range(n_points):
						values.SetValue(var_index, col_offset + col, data)
				else:
					# Fill data points and pad with NaN
					for row, value in enumerate(data):
						values.SetValue(var_index, col_offset + row, value)
					for row in range(len(data), n_points):
						values.SetValue(var_index, col_offset + row, nan)
			col_offset += n_points
		
		# Save to .mat format
		with open(os.path.join(self.__getResultPath(), "observer_data.mat"), "wb") as file:
			stream = OutputStream(file)
			mat.Write(stream)
		
		# Save to .csv format
		with open(os.path.join(self.__getResultPath(), "observer_data.csv"), "w") as file:
			# Write variable names
			file.write(";".join(variables) + "\n")
			# Write values
			for col in range(nDataPointsSum):
				row_data = []
				for var_index in range(len(variables)):
					value = values.GetValue(var_index, col)
					row_data.append(str(value) if value != nan else "")
				file.write(";".join(row_data) + "\n")
		
	def __transitionActive(self, transition):
		"""
		Activates a transition and maps values between modes.
		"""
		from Transition import Transition
		oldMode = self.__actMode
		self.set_active_mode(transition.post)
		self.__compileMode(self.__actMode)
		mappedValues = Transition.mapping(transition, oldMode, self.__actMode)
		self.__actMode.write_init(mappedValues)
		if hasattr(transition, "init_function"):
			transition.init_function(self.__actMode, oldMode)
		
	# Public methods
	def clean(self):
		"""
		Cleans up simulation files and directories.
		"""
		self.shutdown()
		self.__deleteFileSafe(self.__logPath)
		self.__deleteFolderSafe(self.__getOutputPath())
		self.__deleteFolderSafe(self.__getResultPath())
		
	def getCurrentSimulationNumber(self):
		return self.__currentNum
		
	def getPath(self):
		return self.__path
		
	def set_active_mode(self, newMode):
		self.__actMode = newMode
		
	def shutdown(self):
		PySimLib.Log.SetTarget(None)
		if self.__logFile:
			self.__logFile.close()
		
	def simulate(self):
		"""
		Runs the simulation process, including mode transitions and result processing.
		"""
		simTime = 0
		readTime = 0
		
		self.__init()
		self.__prepareFolders()
		self.__preprocess()
		
		self.currentTime = self.startTime
		
		while self.currentTime < self.stopTime:
			# Run simulation
			simTime += self.__actMode.simulate()
			t1 = time.perf_counter()
			result = self.__actMode.read_last_result()
			t2 = time.perf_counter()
			readTime += t2 - t1
			
			# Process results
			self.__observe(result.GetValues())
			lastTimeValue = self.__observer["time"][-1][-1]
			if lastTimeValue < self.currentTime:
				from exceptions.SimulationRanBackwardsException import SimulationRanBackwardsException
				raise SimulationRanBackwardsException()
			self.currentTime = lastTimeValue
			
			print(f"Simulation {self.__currentNum} ended at {self.currentTime}")
			if self.currentTime >= self.stopTime:
				print("Simulation done")
				break
			transition = self.__actMode.find_transition()
			if not transition:
				print(f"Error, no transition found for mode {self.__actMode.id}")
				return
			self.__transitionActive(transition)
			self.__currentNum += 1
		
		self.__save_observer()
		self.__drawPlots()
		
		for m in self.modes:
			m.tool.Close()
		if self.default_tool:
			self.default_tool.Close()