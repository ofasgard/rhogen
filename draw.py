import util
import cairo, math
	
def get_system_size(system):
	# get the diameter of a system in AU by finding the furthest planet and adding 10%
	distances = [planet.distance for planet in system.planets]
	min_distance = min(distances)
	max_distance = max(distances)
	return [min_distance, max_distance]
	
def get_star_color(system):
	if system.spectral_class == "A":
		return [1,1,1]
	if system.spectral_class == "F":
		return [1, 1, 0.6]
	if system.spectral_class == "G":
		return [1, 0.98, 0]
	if system.spectral_class == "K":
		return [1, 0.68, 0]
	if system.spectral_class == "M":
		return [1, 0, 0]
	raise ValueError("Unrecognised spectral class!")
	
def get_orbit_radius(system, planet):
	# get the radius of a planet's orbit as a proportion of the canvas size
	# converts distances into log distances
	sizes = get_system_size(system)
	sizes_km = [util.au_to_km(size) for size in sizes]
	distance_km = util.au_to_km(planet.distance)
	
	min_size_log = math.log(sizes_km[0], 10)
	max_size_log = math.log(sizes_km[1], 10)
	distance_log = math.log(distance_km, 10)
	
	# log distance needs to be mapped onto a value between 0.05 and 0.5
	distance_span = max_size_log - min_size_log
	radius_span = 0.5 - 0.05
	
	scale_value = float(distance_log - min_size_log) / float(distance_span)
	return 0.05 + (scale_value * radius_span)

	
def draw_system(system, canvas_size):
	# initialise surface
	surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, canvas_size, canvas_size)
	ctx = cairo.Context(surface)
	ctx.scale(canvas_size, canvas_size)
	# fill background
	ctx.set_source_rgb(0, 0, 0)
	ctx.rectangle(0, 0, 1, 1)
	ctx.fill()
	# draw star
	color = get_star_color(system)
	ctx.set_source_rgb(color[0], color[1], color[2])  # Solid color
	ctx.set_line_width(0.01)
	ctx.arc(0.5, 0.5, 0.01, 0, 2*math.pi)
	ctx.fill()
	ctx.stroke()
	# draw orbits
	for planet in system.planets:
		radius = get_orbit_radius(system, planet)
		ctx.set_line_width(0.001)
		ctx.arc(0.5, 0.5, radius, 0, 2*math.pi)
		ctx.stroke()

	
	return surface
	
if __name__ == "__main__":
	import generate
	system = generate.generate_system(3,3,3)
	surface = draw_system(system, 1600)
	surface.write_to_png("test.png")
