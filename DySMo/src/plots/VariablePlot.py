"""
Copyright (C) 2016 Alexandra Mehlhase
Copyright (C) 2025 Zizhe Wang

Original implementation by Alexandra Mehlhase and Amir Czwink.
Updated by Zizhe Wang.

This program is licensed under the GNU General Public License (GPL), version 3 or later.
See the LICENSE file or <http://www.gnu.org/licenses/> for details.
"""

from Plot import Plot

class VariablePlot(Plot):
	"""
	A specialized Plot class for visualizing variables in simulations.
	"""

	def __init__(self):
		"""
		Initializes a new VariablePlot instance.
		"""
		super().__init__()  # Call parent constructor
		self.vars = {}  # Initialize a dictionary to store variable-to-color mappings
		
	def getColor(self, modeId, simId, varName):
		"""
		Retrieves the color associated with a specific variable.
		"""
		return self.vars.get(varName, None)  # Use dictionary's `get` method for simplicity