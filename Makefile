FONTFORGE="$(command -v fontforge)"

name=ReduckSans
# one master for now
#masters=$(shell echo {Regular,Bold}.{Mono,Proportional})
masters=$(shell echo {Light,Bold}.Mono)
#masters=$(shell echo Regular.Mono)
ufos=$(patsubst %,$(name).%.ufo,$(masters))

vf: $(name).Variable.ttf

$(name).Variable.ttf: duck.designspace $(ufos)
	fontmake ./duck.designspace -o variable --output-path=$@

clean:
	rm -rvf glyphs/*/ output $(ufos) $(ufos:.ufo=.otf)

#duck.designspace: duck.dssketch
#	dss -o $@ $^

#all: $(wildcard glyphs/*) $(name).otf

$(ufos): $(name).%.ufo : sfds/%.sfdir #$(patsubst %,sfds/%.sfdir,$(masters))
	fontforge -lang py -c 'ff=fontforge.open("'$^'"); ff.generate("'$@'"); ff.generate("'$(@:.ufo=.otf)'")'

#sfds/Bold.Mono.sfdir: sfds/Regular.Mono.sfdir # $(patsubst %.svg,%.split,$(wildcard glyphs/??????_*.svg))
#	rm -rvf $@
#	cp -rvf $^ $@
#	fontforge -lang py -c 'from sys import argv #\
##	ff=fontforge.open(argv[1]) #\
##		ff.familyname#\
##		ff.save(argv[1])' $^
#	fontforge -lang py -script scripts/fontforge_import_glyph_outlines.py $@ $(wildcard glyphs/*.split/bold)
#
#sfds/Regular.Mono.sfdir: $(patsubst %.svg,%.split,$(wildcard glyphs/??????_*.svg))
#	fontforge -lang py -script scripts/fontforge_import_glyph_outlines.py $@ $^

import-glyphs: $(patsubst %.svg,%.split/.duck,$(wildcard glyphs/??????_*.svg))
	fontforge -lang py -script scripts/fontforge_import_glyph_outlines.py sfds/Light.Mono.sfdir $(dir $^) .light
	fontforge -lang py -script scripts/fontforge_import_glyph_outlines.py sfds/Bold.Mono.sfdir $(dir $^) .bold

# extract glyphs
.PRECIOUS: wildcard glyphs/%.split/.duck
glyphs/%.split/.duck: glyphs/%.split.pre/.duck
	mkdir -p $(dir $@)
	./scripts/polygonise_extracted_glyphs.sh $(dir $@) $(dir $^)
	touch $@

.PRECIOUS: wildcard glyphs/%.split.pre/.duck
glyphs/%.split.pre/.duck: glyphs/%.svg
	mkdir -p $(dir $@)
	#./scripts/get_glyph_paths.py < $^ | ./scripts/generate_inkscape_commands.sh $^ $@ | inkscape --shell
	./scripts/split_glyphs.py $^ $(dir $@)
	#./scripts/make_variants.js $(dir $@)
	touch $@

# - through bitmap
#glyphs/%.bitmap: glyphs/%.svg
#	[ -d $@ ] || mkdir -p $@
#	./scripts/get_glyph_paths.py < $^ | ./scripts/generate_inkscape_commands.sh $^ $@ | inkscape --shell
#	touch $@
#glyphs/%.split: glyphs/%.bitmap
#	[ -d $@ ] || mkdir -p $@
#	# trust me this is a legitimate way to use make
#	for i in $$(ls $^); do png2pnm $^/$$i | potrace - -b svg -o $@/$${i%%.png}.svg; done
#	touch $@

