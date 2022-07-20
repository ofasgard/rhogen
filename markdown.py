import util
import string

star_template = string.Template("""
# $name

**$sc-Class**: $description  
**Luminosity**: $luminosity sols  
**Mass**: $mass kg  
**Asteroid Belts**: $belts
""")

planet_template = string.Template("""
## $name

**Distance**: $distance AU  
**Radius**: $radius km  
**Mass**: $mass kg  
**Gravity**: $gravity g  
**Year Length**: $year days  
**Surface Temperature**: $temperature °C  
**Atmosphere**: $atmosphere  
**Biosphere**: $biosphere  
""")

def export_star(star):
	mass_kg = util.stellar_mass_to_kg(star.mass)
	mass_rounded = '{:0.3e}'.format(mass_kg)
	
	if len(star.belts) == 0:
		belts_str = "none"
	else:
		belts_array = ["%0.2f AU" % x for x in star.belts]
		belts_str = ", ".join(belts_array)
	
	output = star_template.substitute(name=star.name, sc=star.spectral_class, description=star.description, luminosity=star.luminosity, mass=mass_rounded, belts=belts_str)
	for planet in star.planets:
		output += export_planet(planet)
	return output

def export_planet(planet):
	distance_au = round(planet.distance, 2)
	radius_km = int(round(util.planetary_radius_to_km(planet.radius), 0))
	mass_kg = util.planetary_mass_to_kg(planet.mass)
	mass_rounded = '{:0.3e}'.format(mass_kg)
	gravity = round(planet.gravity, 2)
	year_length = round(planet.year_length, 1)
	temperature_c = round(util.kelvin_to_celsius(planet.temperature), 1)
	return planet_template.substitute(name=planet.name, distance=distance_au, radius=radius_km, mass=mass_rounded, gravity=gravity, year=year_length, temperature=temperature_c, atmosphere=planet.atmosphere.value, biosphere=planet.biosphere.value)

