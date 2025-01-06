"""
Copyright (C) 2016 Alexandra Mehlhase
Copyright (C) 2025 Zizhe Wang

Original implementation by Alexandra Mehlhase and Amir Czwink.
Updated by Zizhe Wang.

This program is licensed under the GNU General Public License (GPL), version 3 or later.
See the LICENSE file or <http://www.gnu.org/licenses/> for details.
"""

from Definitions import *;

class Plot:
	"""
	A base class for creating and managing plots in the DySMo framework.
	Provides basic grid settings, axis labels, and color management.
	"""

	def __init__(self):
		"""
		Initializes a new Plot instance with default settings.
		"""
		self.drawGrid = True
		self.labelXAxis = ""
		self.labelYAxis = ""
		self.xAxisVar = 'time'
		
	def colorToColorString(self, color):
		"""
		Maps a predefined color constant to a string used by plotting libraries.
		"""
		if(color == Color.BLACK):
			return 'k'
		if(color == Color.BLUE):
			return 'b'
		if(color == Color.CYAN):
			return 'c'
		if(color == Color.GREEN):
			return 'g'
		if(color == Color.MAGENTA):
			return 'm'
		if(color == Color.RED):
			return 'r'
		if(color == Color.YELLOW):
			return 'y'
		
		raise Exception(f"Illegal color: {color}")
		
	def getColor(self, modeId, simId, varName):
		"""
		Abstract method to determine the color for a given plot element.
		"""
		raise NotImplementedError("Method 'getColor' of Class 'Plot' is abstract.")