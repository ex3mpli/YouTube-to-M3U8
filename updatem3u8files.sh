#!/bin/bash
echo $(dirname $0)
python3 -m pip install requests
cd $(dirname $0)/scripts/
python3 abscbnentertainment.py > ../streams/abscbnentertainment.m3u8
python3 gmanetwork.py > ../streams/gmanetwork.m3u8
python3 gmanews.py > ../streams/gmanews.m3u8
python3 gmapublicaffairs.py > ../streams/gmapublicaffairs.m3u8
python3 TV5Philippines.py > ../streams/TV5Philippines.m3u8
python3 DZRHTV.py > ../streams/DZRHTV.m3u8
python3 TeleradyoSerbisyo.py > ../streams/TeleradyoSerbisyo.m3u8
python3 ptvph.py > ../streams/ptvph.m3u8
python3 UNTVNewsandRescue.py > ../streams/UNTVNewsandRescue.m3u8
python3 TVMariaLIVE.py > ../streams/TVMariaLIVE.m3u8
python3 MCGIChannel.py > ../streams/MCGIChannel.m3u8
python3 GCTVASIA.py > ../streams/GCTVASIA.m3u8
python3 LIFETVASIAOFFICIAL.py > ../streams/LIFETVASIAOFFICIAL.m3u8
python3 NET25TV.py > ../streams/NET25TV.m3u8
python3 JIOSWMofficial.py > ../streams/JIOSWMofficial.m3u8
python3 DZRJ810AMRadyoBandido.py > ../streams/DZRJ810AMRadyoBandido.m3u8
python3 TruthChannel.py > ../streams/TruthChannel.m3u8
python3 VeritasPHdotnet.py > ../streams/VeritasPHdotnet.m3u8
python3 DWIZ882Live.py > ../streams/DWIZ882Live.m3u8
echo m3u8 grabbed
