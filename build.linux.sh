#!/bin/bash
pyinstaller -y --onefile --distpath ./dist/linux --clean --name FocusApp --add-data "./favicon.gif:./" main.py
rm -rf build/