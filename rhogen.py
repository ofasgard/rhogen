#!/usr/bin/env python3

import generate
import argparse, json, sys

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-H", "--habitable", help="Desired number of 'habitable' planets to generate. [DEFAULT: 1]", type=int, default=1)
parser.add_argument("-T", "--terrestrial", help="Desired number of terrestrial planets to generate. [DEFAULT: 3]", type=int, default=3)
parser.add_argument("-G", "--giant", help="Desired number of gas giants to generate. [DEFAULT: 3]", type=int, default=3)
parser.add_argument("-f", "--force-habitable", help="Only generate stars that are likely support habitable planets.", action="store_true", default=False)
parser.add_argument("-z", "--max-cycles", help="Maximum cycles to attempt for planet generation before giving up. [DEFAULT: 100]", type=int, default=100)
parser.add_argument("-oJ", "--output-json", help="Path to save a JSON output file containing the generated system.", type=str)
args = parser.parse_args()

def export_json(system):
	return json.dumps(system, default=lambda x: x.__dict__)

if __name__ == "__main__":
	output_check = [x != None for x in [args.output_json]]
	if not any(output_check):
		print("You must specify at least one output type!")
		sys.exit()

	system = generate.generate_system(args.habitable, args.terrestrial, args.giant, habitable_only=args.force_habitable, max_cycles=args.max_cycles)

	if args.output_json != None:
		jsondata = export_json(system)
		try:
			fd = open(args.output_json, "w")
			fd.write(jsondata)
			fd.close()
			print("Successfully wrote system JSON to '%s'!" % args.output_json)
		except OSError as e:
			print("Failed to write system JSON to '%s': %s" % (args.output_json, str(e)))


