#!/bin/bash
pyinstaller -y -w -i logo.icns --onefile --distpath ./dist/mac --clean --name FocusApp --add-data "./favicon.gif:./" main.py
rm dist/mac/FocusApp
rm -rf build/