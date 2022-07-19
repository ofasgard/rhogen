import util
import cairo, math
	
def get_system_size(system):
	# get the diameter of a system in AU by finding the furthest planet and adding 10%
	distances = [planet.distance for planet in system.planets]
	min_distance = min(distances)
	max_distance = max(distances)
	return [min_distance, max_distance]
	
def get_star_color(system):
	pattern = cairo.RadialGradient(0.5, 0.5, 0.003, 0.5, 0.5, 0.03)
	pattern.add_color_stop_rgb(1.0, 0, 0, 0)
	
	if system.spectral_class == "A":
		pattern.add_color_stop_rgb(0.2, 1, 1, 1)
	if system.spectral_class == "F":
		pattern.add_color_stop_rgb(0.2, 1, 1, 0.6)
	if system.spectral_class == "G":
		pattern.add_color_stop_rgb(0.2, 1, 0.98, 0)
	if system.spectral_class == "K":
		pattern.add_color_stop_rgb(0.2, 0.95, 0.65, 0)
	if system.spectral_class == "M":
		pattern.add_color_stop_rgb(0.2, 1, 0, 0)
	return pattern
	
def get_orbit_radius(system, planet):
	# returns the size of each orbit as a proportion of the canvas size (not to scale)
	# divides the available room (between 0.05 and 0.5) into equal segments based on how many planets there are
	planet_count = len(system.planets)
	min_size = 0.05
	max_size = 0.5
	size_spread = max_size - min_size
	size_increment = size_spread / planet_count
	return size_increment * (system.planets.index(planet) + 1)

def get_planet_radius(planet):
	if planet.radius < 0.5:
		return 0.005
	elif planet.radius < 2.0:
		return 0.01
	else:
		return 0.023
	
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
	pattern = get_star_color(system)
	ctx.set_source(pattern)
	ctx.set_line_width(0.01)
	ctx.arc(0.5, 0.5, 0.03, 0, 2*math.pi)
	ctx.fill()
	ctx.stroke()
	# now for the orbits and planets
	for planet in system.planets:
		# orbits
		ctx.set_source_rgb(1,1,1)
		radius = get_orbit_radius(system, planet)
		ctx.set_line_width(0.001)
		ctx.arc(0.5, 0.5, radius, 0, 2*math.pi)
		ctx.stroke()
		ctx.new_path()
		# orbital labels
		ctx.move_to(0.49, 0.51 + radius)
		ctx.set_font_size(0.01)
		ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
		ctx.show_text("%s AU" % round(planet.distance, 2))
		ctx.new_path()
		# planets
		planet_x = 0.5 + radius
		planet_y = 0.5
		ctx.arc(planet_x, planet_y, get_planet_radius(planet), 0, 2*math.pi)
		ctx.fill()
		ctx.stroke()
		# planetary labels
		planet_label_x = planet_x
		planet_label_y = planet_y + 0.03
		ctx.move_to(planet_label_x, planet_label_y)
		ctx.set_font_size(0.007)
		ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
		ctx.show_text(planet.name)
		ctx.new_path()

	return surface
	
if __name__ == "__main__":
	import generate
	system = generate.generate_system(3,3,3)
	system.name_star("Samarkand")
	surface = draw_system(system, 1600)
	surface.write_to_png("test.png")
