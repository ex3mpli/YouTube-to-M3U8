#!/bin/bash
echo $(dirname $0)
python3 -m pip install requests
cd $(dirname $0)/scripts/
python3 abscbn.py > ../streams/abscbn.m3u8
python3 gmanetwork.py > ../streams/gmanetwork.m3u8
python3 gmanews.py > ../streams/gmanews.m3u8
echo m3u8 grabbed
