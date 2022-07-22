from cosmos.star import Star, SpectralClass
from cosmos.planet import Planet
from cosmos.belt import Belt
import random

# The vast majority of the data and equations used by this tool come from the "Worldbuilding" page on the Atomic Rockets website.
# For more information, see: http://www.projectrho.com/public_html/rocket/worldbuilding.php

star_table = [
	(9, "A"),
	(18, "F"),
	(28, "G"),
	(46, "K"),
	(100, "M")
]

habitable_radii = [0.5, 1.5]
habitable_gravities = [0.4, 1.6]

terrestrial_radii = [0.2, 2.0]
terrestrial_gravities = [0.1, 2.0]

giant_radii = [4.0, 15.0]
giant_gravities = [10.0, 20.0]

def generate_star(spectral_class=None):
	if spectral_class == None:
		# if spectral class was not specified, roll on the star table
		roll = random.randint(1, 100)
		spectral_class = next(x[1] for x in star_table if roll <= x[0])
	star_class = SpectralClass[spectral_class]
	star_info = star_class.value
	# generate a random number between 0.01 and 1.00 to use as a factor for the star's luminosity and mass
	star_factor = round(random.uniform(0.01, 1.00), 4)
	luminosity = round(star_info["luminosity"][0] + ((star_info["luminosity"][1] - star_info["luminosity"][0]) * star_factor), 4)
	mass = round(star_info["mass"][0] + ((star_info["mass"][1] - star_info["mass"][0]) * star_factor), 4)
	return Star(star_class.name, star_info["description"], luminosity, mass)
	
def generate_planet(parent_star, distance_range, radius_range, gravity_range):	
	# get the star's possible stable orbits and figure out which ones are valid for the distance range
	possible_orbits = parent_star.get_stable_orbits()
	valid_orbits = [x for x in possible_orbits if (x >= distance_range[0]) and (x <= distance_range[1])]
	# remove any orbits that are already occupied
	existing_orbits = parent_star.get_orbits()
	valid_orbits = [x for x in valid_orbits if x not in existing_orbits]
	# try to select a valid orbit
	if len(valid_orbits) == 0:
		return None
	distance = random.choice(valid_orbits)	
	# radius and gravity are related to each other
	planet_factor = round(random.uniform(0.01, 1.00), 4)
	radius = round(radius_range[0] + ((radius_range[1] - radius_range[0]) * planet_factor), 4)
	gravity = round(gravity_range[0] + ((gravity_range[1] - gravity_range[0]) * planet_factor), 4)
	return Planet(distance, radius, gravity, parent_star.luminosity, parent_star.mass)

generate_habitable_planet = lambda parent : generate_planet(parent, parent.habitable_zone, habitable_radii, habitable_gravities)
generate_terrestrial_planet = lambda parent : generate_planet(parent, [parent.inner_limit, parent.snow_line], terrestrial_radii, terrestrial_gravities)
generate_gas_giant = lambda parent : generate_planet(parent, [parent.snow_line, parent.outer_limit], giant_radii, giant_gravities)

def generate_belt(parent_star):
	# get the star's possible stable orbits and remove any orbits which are already occupied
	possible_orbits = parent_star.get_stable_orbits()
	existing_orbits = parent_star.get_orbits()
	valid_orbits = [x for x in possible_orbits if x not in existing_orbits]
	# try to select a valid orbit
	if len(valid_orbits) == None:
		return None
	distance = random.choice(valid_orbits)
	return Belt(distance)

def generate_system(habitable_quota, terrestrial_quota, giant_quota, belt_quota, spectral_class=None, max_cycles=100):
	star = generate_star(spectral_class)

	count = 0
	for i in range(max_cycles):
		if count >= giant_quota:
			break
		candidate = generate_gas_giant(star)
		if candidate != None and star.add_planet(candidate):
			count += 1
	
	count = 0
	for i in range(max_cycles):
		if count >= habitable_quota:
			break
		candidate = generate_habitable_planet(star)
		if candidate != None and star.add_planet(candidate):
			count += 1
	
	count = 0
	for i in range(max_cycles):
		if count >= terrestrial_quota:
			break
		candidate = generate_terrestrial_planet(star)
		if candidate != None and star.add_planet(candidate):
			count += 1
			
	count = 0
	for i in range(max_cycles):
		if count >= belt_quota:
			break
		candidate = generate_belt(star)
		if star.add_belt(candidate):
			count += 1

	return star

