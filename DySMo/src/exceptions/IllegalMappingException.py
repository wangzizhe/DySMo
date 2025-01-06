"""
Copyright (C) 2016 Alexandra Mehlhase
Copyright (C) 2025 Zizhe Wang

Original implementation by Alexandra Mehlhase and Amir Czwink.
Updated by Zizhe Wang.

This program is licensed under the GNU General Public License (GPL), version 3 or later.
See the LICENSE file or <http://www.gnu.org/licenses/> for details.
"""

from exceptions.ModeException import ModeException

class IllegalMappingException(ModeException):
	"""
	Exception raised for an illegal variable mapping in a mode transition.
	"""

	def __init__(self, fromMode, fromVar, transition, toVar):
		"""
		Initializes the exception with details about the mapping.
		"""
		super().__init__()
		self.__fromMode = fromMode
		self.__fromVar = fromVar
		self.__transition = transition
		self.__toVar = toVar
		
	def __str__(self):
		"""
		Returns a descriptive string representation of the exception.
		"""
		return (
			f"Illegal mapping ({self.__fromVar} -> {self.__toVar}) "
			f"in transition {self.__transition.get_id()} "
			f"from Mode {self.__fromMode.get_id()}."
		)
