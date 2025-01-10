"""
Copyright (C) 2016 Alexandra Mehlhase
Copyright (C) 2025 Zizhe Wang

Original implementation by Alexandra Mehlhase and Amir Czwink.
Updated by Zizhe Wang.

This program is licensed under the GNU General Public License (GPL), version 3 or later.
See the LICENSE file or <http://www.gnu.org/licenses/> for details.
"""

class Transition:
	"""
	Represents a transition between modes in the DySMo framework.
	Handles variable mapping and assigns unique identifiers to transitions.
	"""

	def __init__(self):
		"""
		Initializes a Transition instance with default values.
		"""
		self.__id = None
		
	def get_id(self):
		"""
		Retrieves the unique identifier of the transition.
		"""
		return self.__id
	
	def init(self, id):
		"""
		Initializes the transition with a unique identifier.
		"""
		self.__id = id
		
	# def mapping(self, oldMode, newMode):
	def mapping(self, oldMode, newMode):
		"""
		Handles the mapping of variables between two modes during a transition.
		Args:
		oldMode (Mode): The previous mode object.
		newMode (Mode): The target mode object.
		valuesToSet (dict): The dictionary of values to populate.
		"""
		valuesToSet = {}
		# mapping = self.mapping
		
		for key in self.mapping:
			if key == "*" and self.mapping[key] == "*":
				# self.__map_star(oldMode, newMode, valuesToSet)  # Handles wildcard mapping
				continue
				
			if not oldMode.has_endValue(self.mapping[key]):	
				from exceptions.IllegalMappingException import IllegalMappingException			
				raise IllegalMappingException(oldMode, key, self, self.mapping[key])
				
			valuesToSet[key] = oldMode.get_endValue(self.mapping[key])

		return valuesToSet
	
	# def __map_star(self, oldMode, newMode, valuesToSet):
	# 	"""
	# 	Handles wildcard mapping from old mode to new mode.
	# 	This private method assumes detailed implementation elsewhere.
	# 	"""
	# 	# Implementation of wildcard mapping logic should be placed here.
	# 	# This placeholder method assumes it will map all compatible variables.
	# 	pass
