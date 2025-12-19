#!/usr/bin/env python3

from sys import argv, stdout
import xml.etree.ElementTree as ET
import os
from os.path import basename
import svgpath
import pyclipr
import numpy
import re

NS_SVG="{http://www.w3.org/2000/svg}"

files = []
max_contour_lengths = None
assert len(argv) == 3, "provide an svg file and a directory to save the results to pretty please"

WEIGHTS = [("light", 50), ("bold", 120)]

NS_SVG="{http://www.w3.org/2000/svg}"
NS_INKSCAPE="{http://www.inkscape.org/namespaces/inkscape}"

CSS_DECL_MATCHER = re.compile(r"([a-z-]+) *: *(.+?) *(?:;|$)")

fn = argv[1]
dest = argv[2]
bfn = basename(fn).removesuffix(".svg")

fed = None
#fed = open("/tmp/duck.svg", "w")

with open(fn, "r") as file:
	tree = ET.parse(file)
	stroke_paths = []
	# for the two weights ig
	paths = [[] for _ in WEIGHTS]
	if fed: print(f"<g id=\"src\">", end="", file=fed)
	for j, el in enumerate(tree.iter(NS_SVG+"path")):
		if not el.attrib["d"]: continue
		r = svgpath.parse(el.attrib["d"])
		r = [[y for y in x] for x in svgpath.tree_to_paths(r)]
		for k, path in enumerate(next(svgpath.paths_to_points(r, resolution=5))):
			if fed: print(f"<polyline id=\"d_src{j}_{k}\" points=\"" + " ".join(f"{int(x)},{int(y)}" for x, y in path) + "\" />", end="", file=fed)
			stroke_paths.append((el, numpy.array(path)))
	if fed: print(f"</g>", file=fed)
	max_points = [[] for _ in stroke_paths]
	po = pyclipr.ClipperOffset()
	po.scaleFactor = 1
	for i, (wname, weight) in enumerate(WEIGHTS):
		#print(f"<g class=\"ext\" id=\"ext{i}\">", end="")
		for j, (element, stroke) in enumerate(stroke_paths):
			po.clear()
			po.addPaths([stroke], pyclipr.JoinType.Round, pyclipr.EndType.Round)
			p1 = [numpy.array(a) for a in po.execute(2)]
			po.clear()
			po.addPaths(p1, pyclipr.JoinType.Square, pyclipr.EndType.Polygon)
			p1 = [numpy.array(a) for a in po.execute(weight/2-2)]
			extends = pyclipr.simplifyPaths(p1, 10, False)
			#print(f"expanding path#{j} by {weight/2} yielded these {len(n)} paths")
			#for p in n:
			#	print("M" + "L".join(f"{x} {y}" for x, y in p) + "Z")
			#assert len(n) == 1, f"got {len(n)} paths from a continious segment, what?"
			#for path in extends:
			#	print(f"<polygon id=\"d{i}_ext{j}_{k}\" points=\"" + " ".join(f"{int(x)},{int(y)}" for x, y in path) + "\" />", end="")
			if i == 0 and len(max_points[j]) != len(extends):
				max_points[j] = [0] * len(extends)
			else:
				#for p in extends:
				#	print("M" + "L".join(f"{x} {y}" for x, y in p) + "Z")
				assert len(max_points[j]) == len(extends), f"number of contours changed from {len(max_points[j])} to {len(extends)} in path {j} after changing width to {weight}"
			for k, extend in enumerate(extends):
				if max_points[j][k] < len(extend):
					max_points[j][k] = len(extend)
			# gosh
			paths[i].append([[(float(x), float(y)) for x, y in extend] for extend in extends])
		#print(f"</g>")



print(max_points)
for i in range(len(WEIGHTS)):
	for j in range(len(stroke_paths)):
		for k in range(len(max_points[j])):
			#additional_pts = max_points[j][k] - len(paths[i][j][k])
			pts = paths[i][j][k]
			target_len = max_points[j][k]
			source_len = len(pts)
			print(f"s[{i}][{j}][{k}] = {source_len}; {target_len-source_len}")
			if max_points[j][k] != len(paths[i][j][k]):
				opts = list(pts)
				pts.clear()
				for l in range(max_points[j][k]):
					l2, mix = divmod(l/(target_len-1)*(source_len-1), 1)
					l2 = int(l2)
					pt0 = opts[l2]
					pt1 = opts[l2+1] if mix > 0.001 else pt0
					x = pt0[0] * mix + pt1[0] * (1-mix)
					y = pt0[1] * mix + pt1[1] * (1-mix)
					pts.append((int(x), int(y)))
					#print(f"{l} {l2} {mix:.03f} {x:.02f} {y:.02f}")
			# todo: make this smarter
			#for k in range(additional_pts):
			#	k = k*2 % (len(pts)-1)
			#	x0,y0 = pts[k]; x1,y1 = pts[k+1]
			#	np = ((x0+x1)//2, (y0+y1)//2)
			#	pts.insert(k+1, np)

if fed:
	for i, paths1 in enumerate(paths):
		print(f"<g class=\"ext\" id=\"ext{i}\">", end="", file=fed)
		print(f"<script>trpathdata.push([])</script>", end="", file=fed)
		for j, path in enumerate(paths1):
			pp = ""
			for k, contour in enumerate(path):
				print(f"<polygon id=\"d{i}_ext{j}_{k}\" points=\"" + " ".join(f"{int(x)},{int(y)}" for x, y in contour) + "\" />", end="", file=fed)
				pp += "".join("M" + "L".join(f"{x} {y}" for x, y in path) + "Z" for path in paths[i][j])
			print(f"<script>trpathdata[{i}].push(\"{pp}\")</script>", end="", file=fed)
		print(f"</g>", file=fed)



for i, (wname, _) in enumerate(WEIGHTS):
	for (el, _) in stroke_paths:
		el.attrib["d"] = ""
		el.attrib["style"] = "fill:#000000;stroke:none"
	for j, (el, _) in enumerate(stroke_paths):
		el.attrib["d"] += "".join("M" + "L".join(f"{x} {y}" for x, y in path) + "Z" for path in paths[i][j])
	with open(f"{argv[2]}/{bfn}.{wname}.svg", "wb") as f:
		tree.write(f)

#			xmin = 2000; xmax = -1000; ymin = 2000; ymax = -1000
#			for x, y in contour:
#				if x < xmin: xmin = x
#				if x > xmax: xmax = x
#				if y < ymin: ymin = y
#				if y > ymax: ymax = y
#			if min(x, y) > 60: # if the object is wide or tall enough,
#				pts.append(contour)
#				print(f"{fn}: contour of bounding size {x}x{y}")
#			else:
#				print(f"{fn}: discarding contour of bounding size {x}x{y}")
#		map[el] = pts
#		current_contour_lengths.append([len(x) for x in pts])
#	files.append((fn, tree, els, map))

#	if max_contour_lengths == None:
#		max_contour_lengths = list(current_contour_lengths)
#	else:
#		assert len(max_contour_lengths) == len(current_contour_lengths), f"number of paths mismatches between provided svgs ({fn}: {len(current_contour_lengths)} while first is {len(max_contour_lengths)})"
#	for i, c in enumerate(current_contour_lengths):
#		assert len(max_contour_lengths[i]) == len(c), f"number of path segments mismatches between provided svgs (path {i}, {fn} is {len(c)} while first is {len(max_contour_lengths[i])})"
#		for j in range(len(max_contour_lengths[i])):
#			if max_contour_lengths[i][j] < c[j]:
#				max_contour_lengths[i][j] = c[j]

#for name, tree, els, map in files:
#	for i, el in enumerate(els):
#		ptsg = map[el]
#		path = ""
#		for j, pts in enumerate(ptsg):
#			# todo: make this smarter
#			additional_pts = max_contour_lengths[i][j] - len(pts)
#			print(f"{i} {j}: {len(pts)} {max_contour_lengths[i][j]}, {additional_pts} to add")
#			for k in range(additional_pts):
#				k = k*2 % (len(pts)-1)
#				x0,y0 = pts[k]; x1,y1 = pts[k+1]
#				np = ((x0+x1)//2, (y0+y1)//2)
#				pts.insert(k, np)
#			path += "M" + "L".join(f"{x} {y}" for x, y in pts) + "Z"
#		print(path)
#		el.attrib["d"] = path
	#os.rename(name, name+"~")
	#with open(name, "wb") as f: tree.write(f)
					#print(x, y)
					#print(f"\x1b[{1+int(y/10/2)};{1+int(x/10)}H.", end="", flush=True)
					#n += f"{}"
	#tree.write(stdout.buffer)
#	with open(argv[1].removesuffix(".svg")+".bold.svg", "wb") as f:
#		tree.write(f)
