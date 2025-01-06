"""
Copyright (C) 2016 Alexandra Mehlhase
Copyright (C) 2025 Zizhe Wang

Original implementation by Alexandra Mehlhase and Amir Czwink.
Updated by Zizhe Wang.

This program is licensed under the GNU General Public License (GPL), version 3 or later.
See the LICENSE file or <http://www.gnu.org/licenses/> for details.
"""

from exceptions.ModeException import ModeException;

class MissingTransitionIdException(ModeException):
	"""
	Exception raised when a mode's model is missing the necessary 'transitionId' variable.
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
		return (
			f"The mode {self.__mode} does not contain the required 'transitionId' variable. "
			"Please include it in the model definition."
		)
