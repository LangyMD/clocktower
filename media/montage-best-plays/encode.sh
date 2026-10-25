#!/bin/sh
# frames/ + mix.f32 -> montage-best-plays.mp4
cd "$(dirname "$0")"
ffmpeg -y -loglevel error -framerate 30 -i frames/f%05d.jpg -f f32le -ar 44100 -ac 1 -i mix.f32 \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k -ac 2 -shortest -movflags +faststart montage-best-plays.mp4
