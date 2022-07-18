import util
import math, random

class Planet:
	def __init__(self, distance, radius, gravity, stellar_luminosity, stellar_mass):
		"Orbital Distance: the distance from this planet to its parent body (in AU)."
		self.distance = distance
		"Radius: the radius of the planetary surface, relative to that of Earth (Terra = 1.0)"
		self.radius = radius
		"Gravity: the planet's gravity, measured in G (Terra = 1.0)"
		self.gravity = gravity
		"Mass: the planet's mass relative to that of Earth (Terra = 1.0)"
		self.mass = self.calculate_mass()
		"Roche Limit: the minimum distance a satellite or other body can be without being torn apart (in AU)."
		self.roche_limit = self.calculate_roche_limit()
		"Hill Limit: the maximum distance a satellite or other body can be without being lost (in AU)."
		self.hill_limit = self.calculate_hill_limit(stellar_mass)
		"Year Length: how long this planet's year is in Earth days (Terra = 365)"
		self.year_length = self.calculate_year_length(stellar_mass)
		"Sunlight: the intensity factor of the sunlight this planet receives (Terra = 1.0)"
		self.sunlight = self.calculate_sunlight(stellar_luminosity)
		"Temperature: an approximate figure for the planet's average surface temperature, in Kelvin."
		self.temperature = self.calculate_temperature()
		"Atmosphere: what kind of atmosphere does this planet have, if any?"
		self.atmosphere = self.calculate_atmosphere()
	def calculate_mass(self):
		# The mass of a planet can be calculated using its radius and gravity, inferring its density.
		mass = self.gravity * (self.radius ** 2)
		return mass
	def calculate_roche_limit(self):
		# The Roche Limit is approximately 2.5x the radius of the planet. We multiply this by the radius of Earth to get the distance in AU.
		roche_radius = self.radius * 2.5
		roche_limit_km = util.planetary_radius_to_km(roche_radius)
		roche_limit_au = util.km_to_au(roche_limit_km)
		return roche_limit_au
	def calculate_hill_limit(self, stellar_mass):
		# The Hill Limit is calculated using the distance from the star and the mass of the planet and star.
		# We assume that the planet has negligible eccentricity.
		mass_kg = util.planetary_mass_to_kg(self.mass)
		stellar_mass_kg = util.stellar_mass_to_kg(stellar_mass)
		hill_radius = self.distance * ((mass_kg / (stellar_mass_kg * 3.0)) ** (1/3))
		return hill_radius
	def calculate_year_length(self, stellar_mass):
		# The length a year is a factor of the star's mass (and thus gravity) and of the planet's distance from it.
		year_length = math.sqrt(self.distance ** 3 / stellar_mass)
		return year_length * 365
	def calculate_sunlight(self, stellar_luminosity):
		# The intensity of sunlight a planet receives is a factor of the star's luminosity and the planet's distance.
		sunlight = stellar_luminosity / (self.distance ** 2)
		return sunlight
	def calculate_temperature(self, greenhouse_factor=1.1, albedo=0.3):
		# The approximate temperature can be calculated using the planet's greenhouse factor and albedo, as well as how much sunlight it receives.
		# A planet with no atmosphere has a greenhouse factor of 0; the Earth has a greenhouse factor of 1.1
		# The albedo of Earth is 0.3, and the albedo of Venus is 0.7
		temperature = 374.0 * greenhouse_factor * (1 - albedo) * (self.sunlight ** 0.25)
		return temperature
	def calculate_atmosphere(self):
		# This is probably the most complex calculation; it involves calculating the planet's escape velocity (based on gravity).
		# You can then use this to figure out which gases the planet can hold onto; if it can only hold onto light gases, the atmosphere is thin.
		escape_constant = 2.365 * (10 ** -5)
		meter_radius = util.planetary_radius_to_m(self.radius)
		density_factor = (self.radius ** 3) / self.mass
		density_kg = density_factor * 5500
		escape_velocity = escape_constant * meter_radius * math.sqrt(density_kg)
		jeans_escape_velocity = escape_velocity / 6.00
		# The heuristic we use is whether or not the planet's gravity can hold onto nitrogen gas at the planet's average temperature.
		molar_gas_constant = 8314.41
		nitrogen_weight = 14.0
		nitrogen_velocity = math.sqrt((3.00 * molar_gas_constant * self.temperature) / nitrogen_weight)
		if nitrogen_velocity >= jeans_escape_velocity:
			# The planet cannot hold onto nitrogen; it has only a thin atmosphere.
			return "thin"
		# Next we check whether the planet is beyond the system's snow line (gas giant) or liquid hydrogen line (ice giant).
		if (self.sunlight < 0.0025):
			return "ice giant"
		if (self.sunlight < 0.04):
			return "gas giant"
		# Otherwise, this is a standard kind of terrestrial planet that could have a range of atmospheres.
		return random.choice(["thin", "breathable", "inert", "dense", "corrosive"])

