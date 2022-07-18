import math
	
class Star:
	def __init__(self, spectral_class, description, luminosity, mass):
		"Name: the name of this star."
		self.name = "Nameless Star"
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
		"Planets: a list of Planet objects which are in orbit around this star."
		self.planets = []
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
	def add_planet(self, planet):
		# Add a planet to a star. Returns True if successful, or False if the planet isn't allowed.
		# The planet must be within the star's inner and outer limits.
		if planet.distance < self.inner_limit:
			return False
		if planet.distance > self.outer_limit:
			return False
		# If two planets are closer than the larger planet's roche limit, then the smaller planet will be torn apart.
		for existing_planet in self.planets:
			roche_limit = max(existing_planet.roche_limit, planet.roche_limit)
			distance = abs(planet.distance - existing_planet.distance)
			if distance < roche_limit:
				return False
		# If all checks pass, add the planet.
		self.planets.append(planet)
		self.planets.sort(key=lambda x: x.distance)
		return True		
