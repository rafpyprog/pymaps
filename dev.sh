#!/bin/bash
echo ---------------------------------------------------------------------------
echo RUNNING TESTS
echo ---------------------------------------------------------------------------
python3 -m pytest
if [ $? -eq 1 ]
then
  echo 'Error: tests are not passing.'
  exit 1
fi

PKG_VERSION=`cat ./pymaps/__init__.py | grep -oP '[0-9]{1,2}\.[0-9]{1,2}.[0-9]{1,2}'`
echo ---------------------------------------------------------------------------
echo UPGRADING LOCAL PACKAGE - v$PKG_VERSION
echo ---------------------------------------------------------------------------
pip3 uninstall -y pymaps
python3 setup.py sdist
pip3 install ./dist/pymaps-$PKG_VERSION.tar.gz

echo
echo ---------------------------------------------------------------------------
echo BUILDING PACKAGE DOCUMENTATION
echo ---------------------------------------------------------------------------
cd docs
rm *.ipynb
python3 docs.py
cd ..
