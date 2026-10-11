#!/usr/bin/env bash
# Copies shared design-system files into every app (each app deploys from its own folder).
set -e
cd "$(dirname "$0")/.."
for a in rider driver operator admin; do
  cp shared/k2-ui.css shared/k2-wrap.js shared/k2-mark.svg "$a/"
done
cp shared/k2-mark.svg home/
echo "synced"
