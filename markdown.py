import util
import string

star_template = string.Template("""
# Star

**$sc-Class**: $description  
**Luminosity**: $luminosity sols  
**Mass**: $mass kg  
""")

planet_template = string.Template("""
## Planet

**Distance**: $distance light-minutes  
**Radius**: $radius km  
**Mass**: $mass kg  
**Gravity**: $gravity g  
**Year Length**: $year days  
**Surface Temperature**: $temperature °C  
**Atmosphere**: $atmosphere  
""")

def export_star(star):
	mass_kg = util.stellar_mass_to_kg(star.mass)
	output = star_template.substitute(sc=star.spectral_class, description=star.description, luminosity=star.luminosity, mass=mass_kg)
	for planet in star.planets:
		output += export_planet(planet)
	return output

def export_planet(planet):
	distance_lm = round(util.au_to_lm(planet.distance), 4)
	radius_km = int(round(util.planetary_radius_to_km(planet.radius), 0))
	mass_kg = util.planetary_mass_to_kg(planet.mass)
	gravity = round(planet.gravity, 2)
	year_length = round(planet.year_length, 1)
	temperature_c = round(util.kelvin_to_celsius(planet.temperature), 1)
	return planet_template.substitute(distance=distance_lm, radius=radius_km, mass=mass_kg, gravity=gravity, year=year_length, temperature=temperature_c, atmosphere=planet.atmosphere)
	
if __name__ == "__main__":
	import generate
	system = generate.generate_system(3, 3, 3)
	print(export_star(system))
