#!/bin/bash

PKG_VERSION=`cat ./pymaps/__init__.py | grep -oP '[0-9]{1,2}\.[0-9]{1,2}.[0-9]{1,2}'`
echo $PKG_VERSION

pip3 uninstall -y pymaps
python3 setup.py sdist
pip3 install ./dist/pymaps-$PKG_VERSION.tar.gz
