def km_to_au(km):
	# convert kilometers to astronomical units
	return km / 1.496e+8
	
def au_to_km(au):
	# convert astronomical units to kilometers
	return au * 1.496e+8
	
def planetary_radius_to_km(radius_factor):
	# convert a radius factor given in Terra units to kilometers
	return radius_factor * 6371.00
	
def planetary_radius_to_m(radius_factor):
	# convert a radius factor given in Terra units to meters
	return planetary_radius_to_km(radius_factor) * 1000.00
	
