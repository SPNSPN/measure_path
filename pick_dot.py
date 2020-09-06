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
	parser.add_argument("--th", type = int, default = 10, help = "binarize threshold (default: 10)")
	parser.add_argument("--save", help = "output image")
	return parser.parse_args()

def contour2center (contour):
	m = cv2.moments(contour)
	return (int(m["m10"] / m["m00"]), int(m["m01"] / m["m00"]))

def main (args):
	image = cv2.imread(args.path)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	_, thres = cv2.threshold(gray, args.th, 255, cv2.THRESH_BINARY)
	contours, hierarchy = cv2.findContours(thres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	centers = list(map(contour2center, contours))
	for center in centers:
		print("{0}, {1}".format(*center))
	if args.save:
		image = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
		for center in centers:
			image = cv2.circle(image, center, 5, (255, 0, 0), -1)
		cv2.imwrite(args.save, image)


if __name__ == "__main__":
	main(parse_cmd_args())

