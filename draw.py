import util
import cairo, math
	
def get_system_size(system):
	# get the diameter of a system in AU by finding the furthest planet and adding 10%
	distances = [planet.distance for planet in system.planets]
	max_distance = max(distances)
	return max_distance + (max_distance / 10.0)
	
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

	
	return surface
	
if __name__ == "__main__":
	import generate
	system = generate.generate_system(3,3,3)
	surface = draw_system(system, 1200)
	surface.write_to_png("test.png")
