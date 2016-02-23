#/usr/bin/sh
echo Packing new version..
rm -rv *.pyc
rm -v backend/data/kdd.gz
rm -v backend/data/kdd.names
zip -r nn.$1.zip *
