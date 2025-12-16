#!/bin/bash

define(){ IFS=$'\n' read -r -d '' ${1} || true; }

[ -z "$1" ] && exit 1

mkdir -p "${1%%.svg}"

define filter <<'EOF'
$ARGS.named.filename[:-4] as $dir |
[.[].id] as $layer_ids |

"export-area-drawing",
"export-plain-svg",
(.[] | (
	"file-open:"+$ARGS.named.filename,
	"export-filename:\($dir)/\(.codepoint//.label).svg",
	($layer_ids-[.id] | "select-by-id:\(.[])"),
	"delete-selection",
	"select-by-selector:path",
	"object-stroke-to-path",
	"path-union",
	#"export-id:\(.id)",
	"export-do",
	"file-close"
))
#"file-close"
EOF

exec jq --arg filename "$1" -src "$filter"
