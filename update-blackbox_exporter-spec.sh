#!/bin/sh

set -eu

echo "Checking blackbox_exporter"

PKG="$(
	grep Version: blackbox_exporter.spec \
		| awk '{print $2}'
	)"
RELEASE="$(sed -n 's/^Release: *\([0-9]*\).*$/\1/p' blackbox_exporter.spec)"

echo "Package version: $PKG"

LATEST="$(
	curl -s 'https://github.com/prometheus/blackbox_exporter/releases' \
		| sed -n 's#^.*href="/prometheus/blackbox_exporter/tree/v\([^"-]*\)".*$#\1#p' \
		| head -n1
	)"

echo "Latest version:  $LATEST"

if [ "$LATEST" != "$PKG" ]; then
	printf '%-32s %s -> %s\n' 'blackbox_exporter' "$PKG" "$LATEST"
fi

if [ "$LATEST" != "$PKG" ]; then
	DATE="$(date "+%a %b %d %Y")"
	USER="Lars Kiesow <lkiesow@uos.de>"
	sed -i "s/^Version: .*/Version:       ${LATEST}/" blackbox_exporter.spec
	sed -i "s/^%changelog/%changelog\n\* ${DATE} ${USER} - ${LATEST}-${RELEASE}\n- Update to ${LATEST}\n/" blackbox_exporter.spec

	git commit blackbox_exporter.spec -m "Update blackbox_exporter to ${LATEST}"
fi
