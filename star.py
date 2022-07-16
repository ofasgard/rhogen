import math
	
class Star:
	def __init__(self, spectral_class, description, luminosity, mass):
		"Spectral Class: the type of star in question designated by a single letter, i.e. 'a Class-A star'."
		self.spectral_class = spectral_class
		"Description: some flavour text describing the spectral class of the star."
		self.description = description
		"Luminosity: the luminosity factor of the star (Sol = 1.0)"
		self.luminosity = luminosity
		"Mass: the mass factor of the star (Sol = 1.0)"
		self.mass = mass
		"Inner Limit: the closest orbit a terrestrial planet can occupy within the system (in AU)."
		self.inner_limit = self.calculate_inner_limit()
		"Outer Limit: the furthest orbit any planet can occupy within the system (in AU)."
		self.outer_limit = self.calculate_outer_limit()
		"Habitable Zone: the region within the system that can support water-based life (in AU)."
		self.habitable_zone = self.calculate_habitable_zone()
		"Snow Line: the limit at which terrestrial planets can no longer form, and gas or ice giants form instead (in AU)."
		self.snow_line = self.calculate_snow_line()
	def calculate_inner_limit(self):
		# The star's inner limit is determined by either luminosity or gravity, whichever is higher.
		gravity_limit = 0.2 * self.mass
		luminosity_limit = math.sqrt(self.luminosity / 16.0)
		return max([gravity_limit, luminosity_limit])
	def calculate_outer_limit(self):
		# The star's outer limit is determined exclusively by the gravity of the star.
		gravity_limit = 40.0 * self.mass
		return gravity_limit
	def calculate_habitable_zone(self):
		# The habitable zone is determined exclusively by luminosity. Anything beyond 1.1 is too hot, anything below 0.53 is too cold.
		inner_habitable_limit = math.sqrt(self.luminosity / 1.10)
		outer_habitable_limit = math.sqrt(self.luminosity / 0.53)
		return [inner_habitable_limit, outer_habitable_limit]
	def calculate_snow_line(self):
		# The snow line is determined exclusively by luminosity. When it is below 0.04, enough volatile compounds can condense for gas/ice giants to form.
		snow_line = math.sqrt(self.luminosity / 0.04)
		return snow_line		


