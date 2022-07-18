def integer_to_numeral(number):
	# convert integers to roman numberals (for naming conventions)
	numerals = {1000:'M', 900:'CM', 500:'D', 400:'CD', 100:'C', 90:'XC', 50:'L', 40:'XL', 10:'X', 9:'IX', 5:'V', 4:'IV', 1:'I'}
	roman = ""
	for key in numerals.keys():
		count = int(number / key)
		roman += numerals[key] * count
		number -= key * count
	return roman

def kelvin_to_celsius(kelvin):
	# convert temperatures in kelvin to degrees celsius
	return kelvin - 273.15

def km_to_au(km):
	# convert kilometers to astronomical units
	return km / 1.496e+8
	
def au_to_km(au):
	# convert astronomical units to kilometers
	return au * 1.496e+8
	
def au_to_ls(au):
	# convert astronomical units to light seconds
	return au * 499.005
	
def au_to_lm(au):
	# convert astronomical units to light minutes
	return au_to_ls(au) / 60.0
	
def planetary_radius_to_km(radius_factor):
	# convert a radius factor given in Terra units to kilometers
	return radius_factor * 6371.00
	
def planetary_radius_to_m(radius_factor):
	# convert a radius factor given in Terra units to meters
	return planetary_radius_to_km(radius_factor) * 1000.00
	
def planetary_mass_to_kg(mass_factor):
	# convert a mass factor given in Terra units to kilograms
	return mass_factor * 5.972e+24
	
def stellar_mass_to_kg(mass_factor):
	# convert a mass factor given in Sol units to kilograms
	return mass_factor * 1.989e+30	
	
