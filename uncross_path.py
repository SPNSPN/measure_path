#! /usr/bin/env python3

import os
import sys
import argparse
import math
import numpy
sys.path.remove("/opt/ros/kinetic/lib/python2.7/dist-packages")
import cv2

def parse_cmd_args ():
	parser = argparse.ArgumentParser()
	return parser.parse_args()

def has_cross (pb, pe, qb, qe):
	if pb[0] - pe[0] == 0:
		return (qb[0] - pb[0]) * (qe[0] - pb[0]) < 0
	else:
		m = (pb[1] - pe[1]) / (pb[0] - pe[0])
		c = pb[1] - m * pb[0] 
#	print("debug: hasc: {0}, {1}, {2}, {3}".format(pb, pe, qb, qe))
#	print("debug: yy: {0}, {1}".format(m * qb[0] + c - qb[1], m * qe[0] + c - qe[1]))
		return ((m * qb[0] + c - qb[1]) * (m * qe[0] + c - qe[1])) < 0

def has_cross_in_path (pb, pe, path):
	for pathidx_ in range(len(path) - 1):
		if has_cross(path[pathidx_], path[pathidx_ + 1], pb, pe):
			return True
	return False

def uncross (rest, path):
#	print("debug: path: {0}".format(path))
	if not rest:
		if has_cross_in_path(path[0], path[-1], path):
			return None
		else:
			return path
	for ptidx in range(len(rest)):
		if has_cross_in_path(path[-1], rest[ptidx], path):
			continue
		upath = uncross(rest[:ptidx] + rest[ptidx + 1:], path + [rest[ptidx]])
		if upath:
			return upath
	return None

def sort_chain (rest, chain):
	if not rest:
		return chain
	head = chain[-1]
	nearest_idx, _ = min(enumerate(map(lambda pt: math.sqrt((pt[0] - head[0]) ** 2 + (pt[1] - head[1]) ** 2), rest)), key = lambda elm: elm[1])
	return sort_chain(rest[:nearest_idx] + rest[nearest_idx + 1:], chain + [rest[nearest_idx]])

def main (args):
	centers = list(map(lambda l: list(map(int, l.split(","))), sys.stdin.readlines()))
	centers = sort_chain(centers[1:], [centers[0]])
	uncrosspath = centers
	#uncrosspath = uncross(centers[1:], [centers[0]])
	if not uncrosspath:
		print("WARN: cannot find uncross path.")
		exit()
	for pt in uncrosspath:
		print("{0}, {1}".format(*pt))

if __name__ == "__main__":
	main(parse_cmd_args())

