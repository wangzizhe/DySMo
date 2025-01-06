"""
Copyright (C) 2016 Alexandra Mehlhase
Copyright (C) 2025 Zizhe Wang

Original implementation by Alexandra Mehlhase and Amir Czwink.
Updated by Zizhe Wang.

This program is licensed under the GNU General Public License (GPL), version 3 or later.
See the LICENSE file or <http://www.gnu.org/licenses/> for details.
"""

from exceptions.ModeException import ModeException

class SimulationRanBackwardsException(ModeException):
	"""
	Exception raised when the simulation time moves backwards,
	indicating an invalid simulation state or result.
	"""

	def __init__(self):
		"""
		Initializes the exception.
		"""
		super().__init__()

	def __str__(self):
		"""
		Returns a descriptive string representation of the exception.
		"""
		return "The simulation time moved backwards. This indicates an invalid state or result."