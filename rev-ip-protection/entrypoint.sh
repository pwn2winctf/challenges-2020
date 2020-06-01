#!/bin/bash
if [[ "$#" -ne 1 ]]; then
	echo "usage: $0 license_key"
	exit 1
fi
if ! [[ "$1" =~ ^[0-9]+$ ]]; then
	echo "license_key should be an integer value"
	exit 1
fi
exec make run LICENSE_KEY="$1"
