#!/usr/bin/env python3

from sys import argv
import xml.etree.ElementTree as ET
import os

assert len(argv) == 3, "expecting a file and a directory"

NS_SVG="{http://www.w3.org/2000/svg}"
NS_INKSCAPE="{http://www.inkscape.org/namespaces/inkscape}"

with open(argv[1], "r") as file:
	tree = ET.parse(file)
	parent = tree.find(NS_SVG+"g")
	assert parent.attrib[NS_INKSCAPE+"label"] == "glyphs"
	layers = []
	for layer in list(parent):
		if layer.tag != NS_SVG+"g": continue
		label = layer.attrib[NS_INKSCAPE+"label"]

		code = None
		spacepos = label.find(" ")
		if spacepos != -1:
			code = label[:spacepos]
			label = label[spacepos+1:]

		layers.append((layer, code, label))
		layer.attrib["style"] = layer.attrib["style"].replace("display:none","").removeprefix(";")
		parent.remove(layer)

	print(parent.attrib, len(parent))

	for layer, code, label in layers:
		parent.append(layer)
		nb = ET.tostring(tree.getroot())
		eb = b""
		try:
			with open(f"{argv[2]}/{code or label}.svg", "rb") as file:
				eb = file.read()
		except FileNotFoundError:
			pass
		if eb != nb:
			print(f"{argv[2]}/{code or label}.svg changed")
			with open(f"{argv[2]}/{code or label}.svg", "wb") as file:
				file.write(nb)
		else:
			print(f"{argv[2]}/{code or label}.svg not changed")
		parent.remove(layer)
