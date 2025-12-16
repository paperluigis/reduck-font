#!/usr/bin/env python3
import itertools
import unicodedata

def ascii():
	e=[]
	e.extend(["exclamation","single quote","number sign","dollar","percent","ampersand","single quote","left parenthesis","right parenthesis","asterisk","plus","comma","hyphen","period","slash"])
	e.extend(f"digit {i}" for i in range(10))
	e.extend(["colon","semicolon","less","equal","greater","question"])
	e.extend(f"capital {k}" for k in "abcdefghijklmnopqrstuvwxyz")
	e.extend(["left bracket","backslash","right bracket","caret","underscore"]) # [\]^_
	e.extend(f"small {k}" for k in "abcdefghijklmnopqrstuvwxyz")
	e.extend(["left brace","pipe","right brace","tilde"]) # {|}~

	for p, j in enumerate(e):
		print(f"""<g inkscape:groupmode="layer" id="layer{p+12}" inkscape:label="{p+0x21:04x} {j}" style="display:none"></g>""")

b = []
def unicode_ranges(*e):
	global b
	for p in e:
		if not isinstance(p, int):
			if isinstance(p, str) and len(p) == 1:
				p = ord(p)
			else:
				unicode_ranges(*p)
				continue
		name=unicodedata.name(chr(p),None)
		if not name: continue
		b.append((p, name))

#unicode_ranges(range(0x3040, 0x30a0)) # hiragana

#unicode_ranges(range(0x400, 0x500)) # cyrillic
unicode_ranges("АаБбВвГгҒғДдҘҙЕеЁёЖжЗзИиЙйКкҠҡЛлМмНнҢңОоӨөПпРрСсҪҫТтУуҮүФфХхҺһЦцЧчШшЩщЪъЫыЬьЭэӘәЮюЯя") # cyrillic subset for bashkir

b.sort(key=lambda e: e[0], reverse=True)

for i, (p, name) in enumerate(b):
	print(f"""<g inkscape:groupmode="layer" id="layer{i+2}" inkscape:label="{p:04x} &#{p}; {name}" style="display:none"></g>""")

