FONTFORGE="$(command -v fontforge)"

name=ReduckSans
# one master for now
#masters=$(shell echo {Regular,Bold}.{Mono,Proportional})
masters=$(shell echo {Regular,Bold}.Mono)
#masters=$(shell echo Regular.Mono)
ufos=$(patsubst %,$(name).%.ufo,$(masters))

$(name).Variable.otf: $(ufos)
	fontmake ./duck.designspace -o variable --output-dir=.

#all: $(wildcard glyphs/*) $(name).otf

$(ufos): $(name).%.ufo : sfds/%.sfdir #$(patsubst %,sfds/%.sfdir,$(masters))
	fontforge -lang py -c 'ff=fontforge.open("'$^'"); ff.generate("'$@'"); ff.generate("'$(@:.ufo=.otf)'")'


# extract glyphs
glyphs/%: glyphs/%.svg
	./scripts/get_glyph_paths.py < $^ | ./scripts/generate_inkscape_commands.sh $^ | inkscape --shell
	touch $@

$(name): $(wildcard $(sfdir)/*)
