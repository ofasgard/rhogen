from star import Star
from planet import Planet
import random

# The vast majority of the data and equations used by this tool come from the "Worldbuilding" page on the Atomic Rockets website.
# For more information, see: http://www.projectrho.com/public_html/rocket/worldbuilding.php

star_classes = {}
star_classes["A"] = {"description": "White hue, very bright and hot. Chance for life is very low.", "habitable": False, "luminosity": (14.0, 64.0), "mass": (1.75, 2.18)}
star_classes["F"] = {"description": "Yellow-white hue, brighter and warmer than Sol. Reasonable chance of supporting life.", "habitable": True, "luminosity": (2.4, 8.5), "mass": (1.13, 1.61)}
star_classes["G"] = {"description": "Yellow hue, similar to Sol in luminosity. Chances for life are good.", "habitable": True, "luminosity": (0.61, 1.4), "mass": (0.9, 1.06)}
star_classes["K"] = {"description": "Orange hue, cooler than Sol but with lots of sterilising radiation.", "habitable": True, "luminosity": (0.11, 0.41), "mass": (0.59, 0.88)}
star_classes["M"] = {"description": "Red hue, a very dim and cool star. Chance for life is very low.", "habitable": False, "luminosity": (0.0015, 0.061), "mass": (0.08, 0.45)}

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

def generate_star(habitable_only=False):
	# roll on the star table
	roll = random.randint(1, 100)
	result = next(x[1] for x in star_table if roll <= x[0])
	# if only habitable stars are allowed and this result is not habitable, use recursion to reroll until we get a habitable star
	if habitable_only and not star_classes[result]["habitable"]:
		return generate_star(habitable_only=True)
	star_class = star_classes[result]
	# generate a random number between 0.01 and 1.00 to use as a factor for the star's luminosity and mass
	star_factor = round(random.uniform(0.01, 1.00), 4)
	luminosity = round(star_class["luminosity"][0] + ((star_class["luminosity"][1] - star_class["luminosity"][0]) * star_factor), 4)
	mass = round(star_class["mass"][0] + ((star_class["mass"][1] - star_class["mass"][0]) * star_factor), 4)
	return Star(result, star_class["description"], luminosity, mass)
	
def generate_planet(parent_star, distance_range, radius_range, gravity_range):	
	# distance is independent
	distance = round(random.uniform(distance_range[0], distance_range[1]), 4)
	# radius and gravity are related to each other
	planet_factor = round(random.uniform(0.01, 1.00), 4)
	radius = round(radius_range[0] + ((radius_range[1] - radius_range[0]) * planet_factor), 4)
	gravity = round(gravity_range[0] + ((gravity_range[1] - gravity_range[0]) * planet_factor), 4)
	return Planet(distance, radius, gravity, parent_star.luminosity, parent_star.mass)

generate_habitable_planet = lambda parent : generate_planet(parent, parent.habitable_zone, habitable_radii, habitable_gravities)
generate_terrestrial_planet = lambda parent : generate_planet(parent, [parent.inner_limit, parent.snow_line], terrestrial_radii, terrestrial_gravities)
generate_gas_giant = lambda parent : generate_planet(parent, [parent.snow_line, parent.outer_limit], giant_radii, giant_gravities)	

def generate_system(habitable_quota, terrestrial_quota, giant_quota, habitable_only=False, max_cycles=100):
	star = generate_star(habitable_only)
	
	cycles = 0
	count = 0
	while count < habitable_quota and cycles < max_cycles:
		candidate = generate_habitable_planet(star)
		result = star.add_planet(candidate)
		cycles += 1
		if result == True:
			count += 1
	
	cycles = 0		
	count = 0
	while count < terrestrial_quota and cycles < max_cycles:
		candidate = generate_terrestrial_planet(star)
		result = star.add_planet(candidate)
		cycles += 1
		if result == True:
			count += 1
	cycles = 0		
	count = 0
	while count < giant_quota and cycles < max_cycles:
		candidate = generate_gas_giant(star)
		result = star.add_planet(candidate)
		cycles += 1
		if result == True:
			count += 1

	return star

if __name__ == "__main__":
	test_system = generate_system(2, 3, 3)
	print(test_system.__dict__)
	
	for planet in test_system.planets:
		print(planet.__dict__)
		
	for i in range(1, 1000):
		generate_system(6, 6, 6)

