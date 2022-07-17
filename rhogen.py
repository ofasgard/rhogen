#!/usr/bin/env python3

import generate
import argparse

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-H", "--habitable", help="Desired number of 'habitable' planets to generate. [DEFAULT: 1]", type=int, default=1)
parser.add_argument("-T", "--terrestrial", help="Desired number of terrestrial planets to generate. [DEFAULT: 3]", type=int, default=3)
parser.add_argument("-G", "--giant", help="Desired number of gas giants to generate. [DEFAULT: 3]", type=int, default=3)
parser.add_argument("-f", "--force-habitable", help="Only generate stars that are likely support habitable planets.", action="store_true", default=False)
parser.add_argument("-z", "--max-cycles", help="Maximum cycles to attempt for planet generation before giving up. [DEFAULT: 100]", type=int, default=100)
args = parser.parse_args()

if __name__ == "__main__":
	system = generate.generate_system(args.habitable, args.terrestrial, args.giant, habitable_only=args.force_habitable, max_cycles=args.max_cycles)
	print(system.__dict__)
	
	for planet in system.planets:
		print(planet.__dict__)
