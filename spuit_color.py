#! /usr/bin/env python3

import os
import sys
import argparse
import numpy
sys.path.remove("/opt/ros/kinetic/lib/python2.7/dist-packages")
import cv2

def parse_cmd_args ():
	parser = argparse.ArgumentParser()
	parser.add_argument("path", help = "input image")
	parser.add_argument("--save", help = "output image")
	parser.add_argument("--color", type = int, default = 0xff0000, help = "spuit color (default: 0xff0000)")
	parser.add_argument("--band", type = int, default = 5, help = "band pass range of color code (default: 5)")
	return parser.parse_args()

def int2rgb (c):
	return [(c & 0xff0000) >> 16, (c & 0x00ff00) >> 8, c & 0x0000ff]

def main (args):
	image = cv2.imread(args.path)
	carr = list(reversed(int2rgb(args.color)))
	darr = numpy.array([args.band, args.band, args.band])
	mask = cv2.inRange(image, numpy.array(list(map(lambda c: 0 if c < 0 else c, carr - darr))), numpy.array(list(map(lambda c: 255 if c > 255 else c, carr + darr))))
	result = cv2.bitwise_and(image, image, mask = mask)

	savename = args.save if args.save else "{0}_spuit{1}".format(*os.path.splitext(args.path))

	cv2.imwrite(savename, result)
	print(savename)


if __name__ == "__main__":
	main(parse_cmd_args())

