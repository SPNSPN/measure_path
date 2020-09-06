#! /usr/bin/env python3

import os
import sys
import argparse
import numpy
sys.path.remove("/opt/ros/kinetic/lib/python2.7/dist-packages")
import cv2

def parse_cmd_args ():
	parser = argparse.ArgumentParser()
	return parser.parse_args()

def has_cross (pb, pe, qb, qe):
	m = (pb[1] - pe[1]) / (pb[0] - pe[0])
	c = pb[1] - m * pb[0] 
	print("debug: hasc: {0}, {1}, {2}, {3}".format(pb, pe, qb, qe))
	print("debug: yy: {0}, {1}".format(m * qb[0] + c - qb[1], m * qe[0] + c - qe[1]))
	return ((m * qb[0] + c - qb[1]) * (m * qe[0] + c - qe[1])) < 0

def uncross (rest, path):
	if not rest:
		return path
	for ptidx in range(len(rest)):
		crossing = False
		for pathidx_ in range(len(path) - 1):
			if has_cross(path[pathidx_], path[pathidx_ + 1], path[-1], rest[ptidx]):
				crossing = True
				break
		if crossing:
			continue
		upath = uncross(rest[:ptidx] + rest[ptidx + 1:], path + [rest[ptidx]])
		if upath:
			return upath
	return None

def main (args):
	centers = list(map(lambda l: list(map(int, l.split(","))), sys.stdin.readlines()))
	uncrosspath = uncross(centers[1:], [centers[0]])
	if not uncrosspath:
		print("WARN: cannot find uncross path.")
		exit()
	for pt in uncrosspath:
		print("{0}, {1}".format(*pt))

if __name__ == "__main__":
	main(parse_cmd_args())

