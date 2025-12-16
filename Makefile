FONTFORGE="$(command -v fontforge)"

name=ReduckSans
# one master for now
#masters=$(shell echo {Regular,Bold}.{Mono,Proportional})
masters=$(shell echo {Regular,Bold}.Mono)
#masters=$(shell echo Regular.Mono)
ufos=$(patsubst %,$(name).%.ufo,$(masters))

$(name).Variable.ttf: duck.designspace $(ufos)
	fontmake ./duck.designspace -o variable --output-dir=.

clean:
	rm -rvf glyphs/*/ output $(ufos) $(ufos:.ufo=.otf)

#all: $(wildcard glyphs/*) $(name).otf

$(ufos): $(name).%.ufo : sfds/%.sfdir #$(patsubst %,sfds/%.sfdir,$(masters))
	fontforge -lang py -c 'ff=fontforge.open("'$^'"); ff.generate("'$@'"); ff.generate("'$(@:.ufo=.otf)'")'

sfds/Bold.Mono.sfdir: sfds/Regular.Mono.sfdir # $(patsubst %.svg,%.split,$(wildcard glyphs/??????_*.svg))
	fontforge -lang py -script scripts/fontforge_make_bold.py $@ $^

sfds/Regular.Mono.sfdir: $(patsubst %.svg,%.split,$(wildcard glyphs/??????_*.svg))
	fontforge -lang py -script scripts/fontforge_import_glyph_outlines.py $@ $^

# extract glyphs
# - directly
glyphs/%.split: glyphs/%.svg
	[ -d $@ ] || mkdir -p $@
	./scripts/get_glyph_paths.py < $^ | ./scripts/generate_inkscape_commands.sh $^ $@ | inkscape --shell
	for i in $$(ls $@); do scour -i $@/$$i -o .temp.svg && mv .temp.svg $@/$$i; done
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

