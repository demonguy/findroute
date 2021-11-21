#!/usr/bin/env python

import sys

def load_nav(file):
	data = []
	with open(file) as f:
		_ = f.readline()
		descrption = f.readline()
		_ = f.readline()

		for line in f:
			if line == "99\n":
				break

			l = line.split()
			fix = {}
			fix["lat"] = float(l[0])
			fix["long"] = float(l[1])
			fix["name"] = l[2]
			fix["type"] = l[3]
			fix["region"] = l[4]
			data.append(fix)
	return data

def load_route(file):
	data = []
	with open(file) as f:
		for line in f:
			l = line.split()
			fix = {}
			fix["lat"] = float(l[2])
			fix["long"] = float(l[3])
			fix["orient"] = int(l[5][:-2])
			# fix["name"] = l[2]
			# fix["type"] = l[3]
			# fix["region"] = l[4]
			data.append(fix)
			# print(fix["orient"])
	return data

def find_key_point(route):
	data = []
	last_orient = -100
	for p in route:
		if abs(p["orient"] - last_orient) >= 1:
			data.append(p)
			
		last_orient = p["orient"]

	return data

def distance(a, b):
	return ((a["lat"] - b["lat"])*(a["lat"] - b["lat"])) + ((a["long"] - b["long"])*(a["long"] - b["long"]))


def find_nearest(fixes, point):
	dis = sys.maxsize
	wp = 0
	for fix in fixes:
		d = distance(fix, point)
		if d < dis:
			dis = d
			wp = fix

	return wp


def find_wp(fixes, key_points):
	wps = []
	for p in key_points:
		wp = find_nearest(fixes, p)
		wps.append(wp)

	return wps



r = load_route("C:\Users\cy_ss\Desktop\\123\\1")
kp = find_key_point(r)

fixes = load_nav("C:\Users\cy_ss\Desktop\\123\earth_fix.dat")

wps = find_wp(fixes, kp)

for wp in wps:
	print(wp)