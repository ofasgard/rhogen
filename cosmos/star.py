import util
import enum, math
	
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
		"Asteroid Belts: a list of distances (in AU) that represent asteroid belts in orbit around this star."
		self.belts = []
	def name_star(self, name):
		self.name = name
		planet_number = 1
		for planet in self.planets:
			planet.name = "%s %s" % (name, util.integer_to_numeral(planet_number))
			planet_number += 1	
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
	def get_stable_orbits(self):
		# per artifexian, the ratio of stable orbits between adjacent planets tends to be 1.4-2.0
		# you should use this when adding new celestial bodies to the star, but you don't have to.
		possible_orbits = [ self.inner_limit ]
		while True:
			next_orbit = possible_orbits[-1] * 1.4
			if next_orbit > self.outer_limit:
				break
			else:
				possible_orbits.append(next_orbit)
		return possible_orbits
	def get_orbits(self):
		# returns an ordered list of this system's orbits
		# includes planets and asteroid belts
		orbits = []
		orbits.extend([planet.distance for planet in self.planets])
		orbits.extend([belt.distance for belt in self.belts])
		orbits.sort()
		return orbits
	def is_planet_valid(self, planet):
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
		# The same goes for asteroid belts.
		for belt_radius in self.belts:
			distance = abs(planet.distance - belt_radius)
			if distance < planet.roche_limit:
				return False
		# All checks passed.
		return True	
	def is_belt_valid(self, belt):
		# The belt must be within the star's inner and outer limits.
		if belt.distance < self.inner_limit:
			return False
		if belt.distance > self.outer_limit:
			return False
		# The belt cannot be wtihin another planet's roche limit.
		for planet in self.planets:
			distance = abs(belt.distance - planet.distance)
			if distance < planet.roche_limit:
				return False
		# The belt cannot be within 0.001 AU of another belt.
		for existing_belt in self.belts:
			distance = abs(belt.distance - existing_belt.distance)
			if distance < 0.001:
				return False
		# All checks passed.
		return True
	def add_planet(self, planet):
		# Add a planet to a star. Returns True if successful, or False if the planet isn't allowed.
		if self.is_planet_valid(planet):
			self.planets.append(planet)
			self.planets.sort(key=lambda x: x.distance)
			return True
		else:
			return False	
	def add_belt(self, belt):
		# Add an asteroid belt to a star. Returns True if successful, or False if it isn't allowed.
		if self.is_belt_valid(belt):
			self.belts.append(belt)
			self.belts.sort(key=lambda x: x.distance)
			return True
		else:
			return False

			
class SpectralClass(enum.Enum):
	A = {"description": "White hue, very bright and hot. Chance for life is very low.", "luminosity": (14.0, 64.0), "mass": (1.75, 2.18)}
	F = {"description": "Yellow-white hue, brighter and warmer than Sol. Reasonable chance of supporting life.", "luminosity": (2.4, 8.5), "mass": (1.13, 1.61)}
	G = {"description": "Yellow hue, similar to Sol in luminosity. Chances for life are good.", "luminosity": (0.61, 1.4), "mass": (0.9, 1.06)}
	K = {"description": "Orange hue, cooler than Sol but with lots of sterilising radiation.", "luminosity": (0.11, 0.41), "mass": (0.59, 0.88)}
	M = {"description": "Red hue, a very dim and cool star. Chance for life is very low.", "luminosity": (0.0015, 0.061), "mass": (0.08, 0.45)}
