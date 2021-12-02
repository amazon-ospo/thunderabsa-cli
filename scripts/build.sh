#!/bin/bash
echo "Cleaning folder"
rm -rf build/ dist/ thundera*.egg-info

echo "Updating version"
CURVER=$(cat PKG-INFO | grep 'Metadata-Version:' | cut -d ':' -f2 | tr -d '[:space:]')
NUMVER=$(echo $CURVER | cut -d '.' -f3)
let "NUMVER+=1"
NEWVER=" 0.1."$NUMVER
echo $CURVER "=>" $NEWVER
sed -i "s/$CURVER/$NEWVER/g" PKG-INFO
NEWVER="0.1."$NUMVER
sed -i "s/$CURVER/$NEWVER/g" setup.py

echo "Creating Thundera WHL"
python3 setup.py sdist bdist_wheel > logs/bdist_wheel.log

echo "Checking Thundera WHL"
python3 -m twine check dist/* > logs/twine.log

echo "Cleaning folder"
rm -rf build/ thundera*.egg-info
