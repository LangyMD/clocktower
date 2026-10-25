#!/bin/sh
# frames/ + mix.wav -> explainer-three-tricks.mp4
cd "$(dirname "$0")"
ffmpeg -y -loglevel error -framerate 30 -i frames/f%05d.jpg -i mix.wav \
  -c:v libx264 -preset slow -crf 19 -pix_fmt yuv420p -profile:v high -c:a aac -b:a 192k -shortest -movflags +faststart \
  explainer-three-tricks.mp4
