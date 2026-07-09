#!/bin/bash

if ! [ -f bookbind.py ]; then
   echo "Lacking literally the main program file"
   return
fi

if ! [ -f empty.png ]; then
   echo "Lacking empty.png (aka the image for an filler page)"
   return
fi

if ! [ -f files.txt ]; then
   touch files.txt
fi

if ! [ -d printable ]; then
   mkdir printable
fi

python3 bookbind.py
