For /F "delims=' tokens=2" %%F in ('findstr "[0-9]\.[0-9]" .\pymaps\__init__.py') do (
   set PKG_VERSION=%%F
)

pip uninstall -y pymaps
python setup.py sdist
pip install .\dist\pymaps-%PKG_VERSION%.tar.gz
