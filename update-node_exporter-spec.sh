#!/bin/sh

set -eu

echo "Checking node_exporter"

PKG="$(
	grep Version: node_exporter.spec \
		| awk '{print $2}'
	)"
RELEASE="$(sed -n 's/^Release: *\([0-9]*\).*$/\1/p' node_exporter.spec)"

echo "Package version: $PKG"

LATEST="$(
	curl -s 'https://github.com/prometheus/node_exporter/releases' \
		| sed -n 's#^.*href="/prometheus/node_exporter/tree/v\([^"-]*\)".*$#\1#p' \
		| head -n1
	)"

echo "Latest version:  $LATEST"

if [ "$LATEST" != "$PKG" ]; then
	printf '%-32s %s -> %s\n' 'node_exporter' "$PKG" "$LATEST"
fi

if [ "$LATEST" != "$PKG" ]; then
	DATE="$(date "+%a %b %d %Y")"
	USER="Lars Kiesow <lkiesow@uos.de>"
	sed -i "s/^Version: .*/Version:       ${LATEST}/" node_exporter.spec
	sed -i "s/^%changelog/%changelog\n\* ${DATE} ${USER} - ${LATEST}-${RELEASE}\n- Update to ${LATEST}\n/" node_exporter.spec

	git commit node_exporter.spec -m "Update node_exporter to ${LATEST}"
fi
