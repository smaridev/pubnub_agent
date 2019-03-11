#!/usr/bin/env sh

echo "starting the first script"
python3.5 $SNAP/downstream/downstream.py &
echo "starting the second script"
python3.5 $SNAP/upstream/upstream.py
