#!/bin/bash

define(){ IFS=$'\n' read -r -d '' ${1} || true; }

img="$1"
dir="$2"

[ -z "$dir" ] && exit 1
[ -z "$img" ] && exit 1


define filter <<'EOF'
$ARGS.named.dir as $dir |
$ARGS.named.img as $img |
[.[].id] as $layer_ids |
(. | sort_by(.codepoint)[] | (
	"file-open:"+$img,
	($layer_ids-[.id] | "select-by-id:\(.[])"),
	"delete-selection",
	"select-by-id:\(.id)",
	"selection-unhide",
	"select-clear",

	#"select-by-selector:path",
	#"object-stroke-to-path",
	#"path-union",
	#"select-clear",

	"export-area-page",

	"export-filename:\($dir)/\(.codepoint//.label).svg",
	"export-plain-svg",
	#"export-png-antialias:0",
	"export-do",
	"file-close"
))
#"file-close"
EOF

exec jq --arg dir "$dir" --arg img "$img" -src "$filter"
