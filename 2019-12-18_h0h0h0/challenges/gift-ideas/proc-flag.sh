#!/bin/sh
##
set -eu

FLAG='FLAG-ieviriekaijahhieshai6goh7Lei7phe' \
su \
	-s/bin/sh \
	-c "bin/sleep 36000" \
	nobody &
p=$!

rm -f "${0}"
wait $!
