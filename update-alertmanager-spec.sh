#!/bin/sh

set -eu

echo "Checking Alertmanager"

PKG="$(
	grep Version: alertmanager.spec \
		| awk '{print $2}'
	)"
RELEASE="$(sed -n 's/^Release: *\([0-9]*\).*$/\1/p' alertmanager.spec)"

echo "Package version: $PKG"

LATEST="$(
	curl -s 'https://github.com/prometheus/alertmanager/releases' \
		| sed -n 's_^.*href="/prometheus/alertmanager/tree/v\([^"-]*\)".*$_\1_p' \
		| head -n1
	)"

echo "Latest version:  $LATEST"

if [ "$LATEST" != "$PKG" ]; then
	printf '%-32s %s -> %s\n' 'alertmanager' "$PKG" "$LATEST"
fi

if [ "$LATEST" != "$PKG" ]; then
	DATE="$(date "+%a %b %d %Y")"
	USER="Lars Kiesow <lkiesow@uos.de>"
	sed -i "s/^Version: .*/Version:       ${LATEST}/" alertmanager.spec
	sed -i "s/^%changelog/%changelog\n\* ${DATE} ${USER} - ${LATEST}-${RELEASE}\n- Update to ${LATEST}\n/" alertmanager.spec

	git commit alertmanager.spec -m "Update alertmanager to ${LATEST}"
fi
