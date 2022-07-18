import util
import string

planet_template = string.Template("""
## Planet

**Distance**: $distance light-minutes  
**Radius**: $radius km  
**Gravity**: $gravity g  
**Year Length**: $year days  
**Surface Temperature**: $temperature °C  
**Atmosphere**: $atmosphere  
""")

def export_planet(planet):
	distance_lm = round(util.au_to_lm(planet.distance), 4)
	radius_km = round(util.planetary_radius_to_km(planet.radius), 0)
	gravity = round(planet.gravity, 2)
	year_length = round(planet.year_length, 1)
	temperature_c = round(util.kelvin_to_celsius(planet.temperature), 1)
	return planet_template.substitute(distance=distance_lm, radius=radius_km, gravity=gravity, year=year_length, temperature=temperature_c, atmosphere=planet.atmosphere)
	
if __name__ == "__main__":
	import generate
	system = generate.generate_system(3, 3, 3)
	output = ""
	for planet in system.planets:
		output += export_planet(planet)
	print(output)
