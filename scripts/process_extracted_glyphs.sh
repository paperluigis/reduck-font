old_pwd="$PWD"
dir="$old_pwd/$1"

set -e

cd "$dir"

#for i in *.svg; do
#	case $i in
#		*.*.*) ;;
#		*) "$old_pwd"/scripts/make_variants.js "$i";;
#	esac
#done

#mkdir -p fill

#ls | jq -rR 'select(endswith(".svg")) | "file-open:\(.)",
#"select-by-selector:path",
#"object-stroke-to-path",
#"export-plain-svg",
#"export-area-page",
#"export-filename:fill/\(.)",
#"export-do",
#"file-close"' | inkscape --shell

