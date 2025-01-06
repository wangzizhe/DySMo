"""
Copyright (C) 2016 Alexandra Mehlhase
Copyright (C) 2025 Zizhe Wang

Original implementation by Alexandra Mehlhase and Amir Czwink.
Updated by Zizhe Wang.

This program is licensed under the GNU General Public License (GPL), version 3 or later.
See the LICENSE file or <http://www.gnu.org/licenses/> for details.
"""

from exceptions.ModeException import ModeException

class InvalidModeModelException(ModeException):
	"""
	Exception raised when the model format of a mode is invalid or unsupported.
	"""

	def __init__(self, mode):
		"""
		Initializes the exception with details about the invalid mode.
		"""
		super().__init__()
		self.__mode = mode
		
	def __str__(self):
		"""
		Returns a descriptive string representation of the exception.
		"""
		return f"The model format of {self.__mode} cannot be determined or is invalid."