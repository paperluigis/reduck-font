old_pwd="$PWD"
cd "$2"
set -e
for i in *.svg; do
	echo "$old_pwd/$1/${i%%.svg}.light.svg" "$PWD/$i"
	if [[ "$old_pwd/$1/${i%%.svg}.light.svg" -nt "$i" ]]; then
		echo "$i seems to already be processed"
	else
		echo "$i processing"
		"$old_pwd"/scripts/polygonise_contours.py "$i" "$old_pwd/$1/"
	fi
done
