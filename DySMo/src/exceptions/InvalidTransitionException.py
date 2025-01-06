"""
Copyright (C) 2016 Alexandra Mehlhase
Copyright (C) 2025 Zizhe Wang

Original implementation by Alexandra Mehlhase and Amir Czwink.
Updated by Zizhe Wang.

This program is licensed under the GNU General Public License (GPL), version 3 or later.
See the LICENSE file or <http://www.gnu.org/licenses/> for details.
"""

from exceptions.ModeException import ModeException;

class InvalidTransitionException(ModeException):
	"""
	Exception raised when a mode attempts to activate a transition that it does not contain.
	"""
	
	def __init__(self, mode, transId):
		"""
		Initializes the exception with details about the invalid transition.
		"""
		super().__init__()
		self.__mode = mode
		self.__transId = transId
		
	def __str__(self):
		"""
		Returns a descriptive string representation of the exception.
		"""
		return (
			f"Mode {self.__mode} tried to activate transition {self.__transId}, "
			"but it does not contain this transition."
		)
