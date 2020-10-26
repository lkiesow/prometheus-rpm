#!/bin/sh

set -eu

echo "Checking ssl_exporter"

PKG="$(
	grep Version: ssl_exporter.spec \
		| awk '{print $2}'
	)"
RELEASE="$(sed -n 's/^Release: *\([0-9]*\).*$/\1/p' ssl_exporter.spec)"

echo "Package version: $PKG"

LATEST="$(
	curl -s 'https://github.com/ribbybibby/ssl_exporter/releases' \
		| sed -n 's#^.*href="/ribbybibby/ssl_exporter/tree/v\([^"-]*\)".*$#\1#p' \
		| head -n1
	)"

echo "Latest version:  $LATEST"

if [ "$LATEST" != "$PKG" ]; then
	printf '%-32s %s -> %s\n' 'ssl_exporter' "$PKG" "$LATEST"
fi

if [ "$LATEST" != "$PKG" ]; then
	DATE="$(date "+%a %b %d %Y")"
	USER="Lars Kiesow <lkiesow@uos.de>"
	sed -i "s/^Version: .*/Version:       ${LATEST}/" ssl_exporter.spec
	sed -i "s/^%changelog/%changelog\n\* ${DATE} ${USER} - ${LATEST}-${RELEASE}\n- Update to ${LATEST}\n/" ssl_exporter.spec

	#git commit ssl_exporter.spec -m "Update ssl_exporter to ${LATEST}"
fi
