#!/usr/bin/env python3

import generate, markdown, draw
import argparse, json, sys

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-H", "--habitable", help="Desired number of 'habitable' planets to generate. [DEFAULT: 1]", type=int, default=1)
parser.add_argument("-T", "--terrestrial", help="Desired number of terrestrial planets to generate. [DEFAULT: 3]", type=int, default=3)
parser.add_argument("-G", "--giant", help="Desired number of gas giants to generate. [DEFAULT: 3]", type=int, default=3)
parser.add_argument("-n", "--name", help="Give a name to the star and its planets.", type=str)
parser.add_argument("-c", "--spectral-class", help="Generate a star with a specific spectral class: A, F, G, K or M", type=str)
parser.add_argument("-z", "--max-cycles", help="Maximum cycles to attempt for planet generation before giving up. [DEFAULT: 100]", type=int, default=100)
parser.add_argument("-oJ", "--output-json", help="Path to save a JSON output file containing the generated system.", type=str)
parser.add_argument("-oM", "--output-markdown", help="Path to save a MarkDown output file containing a report about the system.", type=str)
parser.add_argument("-oI", "--output-image", help="Path to save a PNG diagram of the generated system.", type=str)
args = parser.parse_args()

def export_json(system):
	return json.dumps(system, default=lambda x: x.__dict__)

if __name__ == "__main__":
	output_check = [x != None for x in [args.output_json, args.output_markdown, args.output_image]]
	if not any(output_check):
		print("You must specify at least one output type!")
		sys.exit()
		
	if args.spectral_class != None and args.spectral_class not in ["A", "F", "G", "K", "M"]:
		print("Only the following spectral classes are supported: A, F, G, K or M.")
		sys.exit()

	system = generate.generate_system(args.habitable, args.terrestrial, args.giant, spectral_class=args.spectral_class, max_cycles=args.max_cycles)
	
	if args.name != None:
		system.name_star(args.name)

	if args.output_json != None:
		jsondata = export_json(system)
		try:
			fd = open(args.output_json, "w")
			fd.write(jsondata)
			fd.close()
			print("Successfully wrote system JSON to '%s'!" % args.output_json)
		except OSError as e:
			print("Failed to write system JSON to '%s': %s" % (args.output_json, str(e)))

	if args.output_markdown != None:
		markdowndata = markdown.export_star(system)
		try:
			fd = open(args.output_markdown, "w")
			fd.write(markdowndata)
			fd.close()
			print("Successfully wrote MarkDown report to '%s'!" % args.output_markdown)
		except OSError as e:
			print("Failed to write MarkDown report to '%s': %s" % (args.output_markdown, str(e)))
			
	if args.output_image != None:
		try:
			surface = draw.draw_system(system, 1600)
			surface.write_to_png(args.output_image)
			print("Successfully wrote image to '%s'!" % args.output_image)
		except OSError as e:
			print("Failed to write image to '%s': %s" % (args.output_image, str(e)))

