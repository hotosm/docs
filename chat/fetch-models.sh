#!/bin/sh
# Download GGUF models from Hugging Face into /models, resuming on failure.
# Usage: fetch-models.sh <repo> <file> [<repo> <file> ...]
# A copy is inlined in chart/templates/_helpers.tpl (docs-chat.fetchScript).
set -eu

fetch() {
  out="/models/$2"
  if [ -s "$out" ]; then
    echo "Have $2"
    return
  fi
  url="https://huggingface.co/$1/resolve/main/$2"
  for i in $(seq 1 30); do
    echo "Downloading $2 (attempt $i)"
    # Abort stalled transfers (<10KB/s for 30s) and resume from the partial file
    if curl -fL --connect-timeout 20 --speed-limit 10240 --speed-time 30 \
      -C - -o "$out.part" "$url"; then
      mv "$out.part" "$out"
      return
    fi
    sleep 5
  done
  echo "Failed to download $2" >&2
  exit 1
}

while [ $# -ge 2 ]; do
  fetch "$1" "$2"
  shift 2
done
