from sys import argv
import os

sfd = argv[1]
dirs = argv[2:]


glyphs_by_encoding = {}
glyphs_by_name = {}

outlines = {}

for dir in dirs:
	for file in os.listdir(dir):
		name = file[:-4]
		#print(f"{dir}/{file} .. {name}")
		outlines[name] = f"{dir}/{file}"


ff = fontforge.open(sfd)
for glyph in ff.glyphs():
	#glyphs_by_encoding[glyph.encoding] = glyph
	#glyphs_by_name[glyph.glyphname] = glyph
	u = outlines.get(glyph.glyphname, outlines.get(f"{glyph.unicode:04x}"))
	if u:
		glyph.clear(1)
		glyph.importOutlines(u)

ff.save(sfd)

#for k, v in outlines.items():
#	glyph = glyphs_by_encoding.get(int(k, 16), glyphs_by_name.get(k))
#	if glyph == None:
#		print(f"failed to find glyph for '{k}'")
#		continue
#	glyph.importOutlines(v)
