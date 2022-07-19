import util
import cairo, math
	
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
	
def get_planet_color(planet, x, y):
	radius = get_planet_radius(planet)
	pattern = cairo.RadialGradient(x, y, (radius / 10), x, y, radius)
	pattern.add_color_stop_rgb(1.0, 0, 0, 0)
	if planet.atmosphere == "thin":
		pattern.add_color_stop_rgb(0.8, 0.4, 0.4, 0.4)
	if planet.atmosphere == "inert":
		pattern.add_color_stop_rgb(0.8, 0.9, 0.9, 0.9)
	if planet.atmosphere == "breathable":
		pattern.add_color_stop_rgb(0.8, 0.2, 0.3, 0.9)
	if planet.atmosphere == "dense":
		pattern.add_color_stop_rgb(0.8, 0.70, 0.3, 0.3)
	if planet.atmosphere == "corrosive":
		pattern.add_color_stop_rgb(0.8, 0.3, 1.0, 0.3)
	if planet.atmosphere == "gas giant":
		pattern.add_color_stop_rgb(0.8, 1.0, 0.5, 0.5)
	if planet.atmosphere == "ice giant":
		pattern.add_color_stop_rgb(0.8, 0.7, 0.7, 1.0)
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
	if planet.radius <= 0.5:
		return 0.005
	elif planet.radius <= 2.0:
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
	# system label
	ctx.set_source_rgb(1,1,1)
	ctx.set_font_size(0.02)
	ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
	ctx.move_to(0.01, 0.02)
	ctx.show_text("%s System" % system.name)
	ctx.new_path()
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
		pattern = get_planet_color(planet, planet_x, planet_y)
		ctx.set_source(pattern)
		ctx.arc(planet_x, planet_y, get_planet_radius(planet), 0, 2*math.pi)
		ctx.fill()
		ctx.stroke()
		# planetary labels
		ctx.set_source_rgb(1,1,1)
		planet_label_x = planet_x
		planet_label_y = planet_y + 0.03
		ctx.move_to(planet_label_x, planet_label_y)
		ctx.set_font_size(0.0065)
		ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
		ctx.show_text(planet.name)
		ctx.new_path()

	return surface	
