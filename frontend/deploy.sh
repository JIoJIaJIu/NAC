#!/usr/bin/bash
npm install
bower install
gulp
rm -rfv ../backend/public
cp -rv dist ../backend/public
cp -rv bower_components ../backend/public
