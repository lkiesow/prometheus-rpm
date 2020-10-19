#!/bin/sh

set -eu

echo "Checking Prometheus"

PKG="$(
	grep Version: prometheus.spec \
		| awk '{print $2}'
	)"
RELEASE="$(sed -n 's/^Release: *\([0-9]*\).*$/\1/p' prometheus.spec)"

echo "Package version: $PKG"

LATEST="$(
	curl -s 'https://github.com/prometheus/prometheus/releases' \
		| sed -n 's_^.*href="/prometheus/prometheus/tree/v\([^"-]*\)".*$_\1_p' \
		| head -n1
	)"

echo "Latest version:  $LATEST"

if [ "$LATEST" != "$PKG" ]; then
	printf '%-32s %s -> %s\n' 'prometheus' "$PKG" "$LATEST"
fi

if [ "$LATEST" != "$PKG" ]; then
	DATE="$(date "+%a %b %d %Y")"
	USER="Lars Kiesow <lkiesow@uos.de>"
	sed -i "s/^Version: .*/Version:       ${LATEST}/" prometheus.spec
	sed -i "s/^%changelog/%changelog\n\* ${DATE} ${USER} - ${LATEST}-${RELEASE}\n- Update to ${LATEST}\n/" prometheus.spec

	git commit prometheus.spec -m "Update to ${LATEST}"
fi
