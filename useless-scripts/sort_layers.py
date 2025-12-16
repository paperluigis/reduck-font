#!/usr/bin/env python3

from sys import argv
import xml.etree.ElementTree as ET
import os

assert len(argv) == 2, "expecting a single argument"

NS_SVG="{http://www.w3.org/2000/svg}"
NS_INKSCAPE="{http://www.inkscape.org/namespaces/inkscape}"

with open(argv[1], "r") as file:
	tree = ET.parse(file)
	parent = tree.find(NS_SVG+"g")
	assert parent.attrib[NS_INKSCAPE+"label"] == "glyphs"
	layers = []
	for layer in parent:
		if layer.tag != NS_SVG+"g": continue
		label = layer.attrib[NS_INKSCAPE+"label"]
		#code = int(label[:4],16)-0x21
		#label = f"{code:04x} " +label[5:]
		#layer.attrib[NS_INKSCAPE+"label"]=label
		layers.append((label, layer))
	# inkscape shows ts in reverse so we counteract
	layers.sort(key=lambda a: a[0], reverse=True)
	for _, layer in layers:
		parent.remove(layer)
		parent.append(layer)
	with open(argv[1]+".new", "wb") as file:
		tree.write(file)
	os.rename(argv[1], argv[1]+"~")
	os.rename(argv[1]+".new", argv[1])
