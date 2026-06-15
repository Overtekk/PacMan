#!/bin/bash
uv run pyinstaller --clean --onedir --name 'Pac-Man' --noconfirm --windowed \
    --add-data "assets:assets" \
    --add-data "data:data" \
	--copy-metadata arcade \
    --collect-data arcade \
    --add-binary "mazegenerator/mazegenerator-2.0.2-py3-none-any.whl:." \
    src/auto_main.py
