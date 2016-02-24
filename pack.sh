#/usr/bin/sh
echo Packing new version..
rm -rfv frontend/node_modules
rm -rfv frontend/bower_components
rm -rfv frontend/dist

rm -rfv backend/public
rm -rfv backend/dist
rm -rfv backend/build
rm -rfv backend/nn.egg-info

rm -rv *.pyc
rm -v backend/data/kdd.gz
rm -v backend/data/kdd.names
zip -r nn.$1.zip *
