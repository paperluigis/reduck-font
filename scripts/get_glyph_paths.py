#!/usr/bin/env python3

from sys import stdin
import xml.etree.ElementTree as ET
import json

NS_SVG="{http://www.w3.org/2000/svg}"
NS_INKSCAPE="{http://www.inkscape.org/namespaces/inkscape}"

root = ET.parse(stdin).getroot()
parent = root.find(NS_SVG+"g")
assert parent.attrib[NS_INKSCAPE+"label"] == "glyphs"
for layer in parent:
	if layer.tag != NS_SVG+"g": continue
	label = layer.attrib[NS_INKSCAPE+"label"]
	#hex = int(label[:4], 16)
	code = None
	spacepos = label.find(" ")
	if spacepos != -1:
		code = label[:spacepos]
		label = label[spacepos+1:]
	a = { "id": layer.attrib["id"], "codepoint": code, "label": label, "paths": [] }
	for object in layer:
		assert object.tag == NS_SVG+"path"
		a["paths"].append(object.attrib["id"])
	print(json.dumps(a))

