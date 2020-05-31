#!/bin/bash
while true; do
	python tx_on.py
	aplay ve6azx.wav
	timeout 1 speaker-test -t sine -f 800
	python tx_off.py
	timeout 5 arecord -D sysdefault:CARD=1 -d 10 -f cd -t wav f2.wav
	python tx_on.py
	aplay f2.wav
	python tx_off.py
	sleep 30
done
