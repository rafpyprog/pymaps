#!/bin/bash
python3 -m pytest
if [ $? -eq 1 ]
then
  echo 'Error: tests are not passing.'
  exit 1
fi

PKG_VERSION=`cat ./pymaps/__init__.py | grep -oP '[0-9]{1,2}\.[0-9]{1,2}.[0-9]{1,2}'`
echo $PKG_VERSION

pip3 uninstall -y pymaps
python3 setup.py sdist
pip3 install ./dist/pymaps-$PKG_VERSION.tar.gz
