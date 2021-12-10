#!/usr/bin/env python
import os
import sys
import json
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

def load_route_raw(file):
	data = []
	with open(file) as f:
		for line in f:
			l = line.split()
			fix = {}
			fix["lat"] = float(l[2])
			fix["long"] = float(l[3])
			fix["orient"] = int(l[5][:-2])
			fix["height"] = int(l[8].replace(',', ''))
			# fix["name"] = l[2]
			# fix["type"] = l[3]
			# fix["region"] = l[4]
			data.append(fix)
			# print(fix["orient"])
	return data

def load_route(json_file):
	data = []
	with open(json_file) as f:
		r = json.load(f)
		for d in r:
			fix = {}
			fix["lat"] = float(d["latitude"])
			fix["long"] = float(d["longitude"])
			fix["height"] = float(d["height"])
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

	# return data
	return route

def distance(a, b):
	x = abs(a["lat"] - b["lat"])
	y = abs(a["long"] - b["long"])
	if x < 0.5 and y < 0.5:
		return x*x + y*y
	else:
		return 10000


def find_nearest(fixes, point):
	dis = sys.maxsize
	wp = 0
	for fix in fixes:
		d = distance(fix, point)
		if d < dis and ((point["height"] >= 5000 and fix["type"] == "ENRT") or (point["height"] < 5000 and (fix["type"] == sys.argv[1] or fix["type"] == sys.argv[2] or fix["type"] == "ENRT"))):
			dis = d
			wp = fix

	wp["error"] = dis
	wp["height"] = point["height"]
	return wp


def find_wp(fixes, key_points):
	wps = []
	for p in key_points:
		wp = find_nearest(fixes, p)
		wps.append(wp)

	return wps


print(sys.argv[1], sys.argv[2])

r = load_route(os.path.join(os.path.dirname(__file__), "track.json"))
# kp = find_key_point(r)

fixes = load_nav(os.path.join(os.path.dirname(__file__), "earth_fix.dat"))

wps = find_wp(fixes, r)

last = None
for wp in wps:
	if (last and last["name"] == wp["name"]) or wp["error"] > 0.5:
		pass
	else:
		print(wp["name"], wp["type"], wp["height"], float("{:.2f}".format(wp["error"])))

	last = wp
