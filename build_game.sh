#!/bin/bash
uv run pyinstaller --clean --onedir --name 'Pac-Man' --noconfirm --windowed \
    --add-data "assets:assets" \
    --add-data "data:data" \
    --add-data "mazegenerator:mazegenerator" \
    src/auto_main.py

rm -rf dist/Pac-Man/_internal/arcade/VERSION

echo "3.3.3" > dist/Pac-Man/_internal/arcade/VERSION

echo "Success!"
