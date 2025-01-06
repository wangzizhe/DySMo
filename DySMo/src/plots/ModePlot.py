"""
Copyright (C) 2016 Alexandra Mehlhase
Copyright (C) 2025 Zizhe Wang

Original implementation by Alexandra Mehlhase and Amir Czwink.
Updated by Zizhe Wang.

This program is licensed under the GNU General Public License (GPL), version 3 or later.
See the LICENSE file or <http://www.gnu.org/licenses/> for details.
"""

from Definitions import *
from Plot import Plot

class ModePlot(Plot):
	"""
	A specialized Plot class for managing and visualizing simulation modes.
	"""
	
	def __init__(self):
		"""
		Initializes a new ModePlot instance.
		"""
		super().__init__()  # Call parent constructor
		self.__counter = 0  # Decrementing counter for unique variable IDs
		self.__vars = {}  # Dictionary to map variable names to unique counters
		
	def _getVarCounter(self, varName):
		"""
		Retrieves or assigns a unique counter for the given variable.
		"""
		if varName not in self.__vars:
			self.__vars[varName] = self.__counter
			self.__counter -= 1
		return self.__vars[varName]
		
	def getColor(self, modeId, simId, varName):
		"""
		Determines the color for a given variable based on its unique counter and the mode ID.
		"""
		colId = ((self._getVarCounter(varName) + modeId - 1) % 7) + 1
		if varName in self.vars:
			return Color(colId)
		return None