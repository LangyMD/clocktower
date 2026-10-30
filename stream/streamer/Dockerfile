# The 24/7 YouTube streamer: ffmpeg + a small Python loop. Build from the repo root:
#   docker build -f stream/streamer/Dockerfile -t clocktower-stream stream/streamer
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg ca-certificates && rm -rf /var/lib/apt/lists/* \
 && pip install --no-cache-dir "huggingface_hub>=0.24"
WORKDIR /app
COPY stream.py /app/stream.py
ENV MEDIA_DIR=/data/stream PYTHONUNBUFFERED=1
VOLUME /data
CMD ["python3", "/app/stream.py"]
