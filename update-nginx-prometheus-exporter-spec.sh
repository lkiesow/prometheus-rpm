#!/bin/sh

set -eu

echo "Checking nginx-prometheus-exporter"

PKG="$(
	grep Version: nginx-prometheus-exporter.spec \
		| awk '{print $2}'
	)"
RELEASE="$(sed -n 's/^Release: *\([0-9]*\).*$/\1/p' nginx-prometheus-exporter.spec)"

echo "Package version: $PKG"

LATEST="$(
	curl -s 'https://github.com/nginxinc/nginx-prometheus-exporter/releases' \
		| sed -n 's#^.*href="/nginxinc/nginx-prometheus-exporter/tree/v\([^"-]*\)".*$#\1#p' \
		| head -n1
	)"

echo "Latest version:  $LATEST"

if [ "$LATEST" != "$PKG" ]; then
	printf '%-32s %s -> %s\n' 'nginx-prometheus-exporter' "$PKG" "$LATEST"
fi

if [ "$LATEST" != "$PKG" ]; then
	DATE="$(date "+%a %b %d %Y")"
	USER="Lars Kiesow <lkiesow@uos.de>"
	sed -i "s/^Version: .*/Version:       ${LATEST}/" nginx-prometheus-exporter.spec
	sed -i "s/^%changelog/%changelog\n\* ${DATE} ${USER} - ${LATEST}-${RELEASE}\n- Update to ${LATEST}\n/" nginx-prometheus-exporter.spec

	git commit nginx-prometheus-exporter.spec -m "Update nginx-prometheus-exporter to ${LATEST}"
fi
