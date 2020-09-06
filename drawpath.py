#! /usr/bin/env python3

import os
import sys
import argparse
import numpy
sys.path.remove("/opt/ros/kinetic/lib/python2.7/dist-packages")
import cv2

def parse_cmd_args ():
	parser = argparse.ArgumentParser()
	parser.add_argument("image", help = "base image file")
	parser.add_argument("--save",help = "save image file")
	return parser.parse_args()

def main (args):
	centers = list(map(lambda l: tuple(map(int, l.split(","))), sys.stdin.readlines()))
	image = cv2.imread(args.image)

	for idx in range(len(centers) - 1):
		image = cv2.line(image, centers[idx], centers[idx + 1], (0, 255, 0), 2)
	image = cv2.line(image, centers[-1], centers[0], (0, 255, 0), 2)

	savename = args.save if args.save else "{0}_path{1}".format(*os.path.splitext(args.image))
	cv2.imwrite(savename, image)

if __name__ == "__main__":
	main(parse_cmd_args())

