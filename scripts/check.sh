#!/bin/bash
echo "Checking PEP8"
$HOME/.local/bin/pycodestyle --exclude='*testfiles*' . | grep -v 'build' | grep -v 'dist' | grep -v 'W605'> logs/pep8.log

echo "Creating Thundera ENV"
$HOME/.local/bin/virtualenv thundera_env > logs/virtualenv.log

echo "Activating Thundera ENV"
source thundera_env/bin/activate

echo "Removing old Thundera WHL"
pip3 uninstall thundera-bsa -y > logs/pip3uninstall.log

echo "Installing old Thundera WHL"
python3 setup.py install > logs/pip3install.log

echo "Running Thundera WHL"
rm -rf *.csv
#thundera ./testfiles/folder/
#thundera ./thundera/
#thundera /dev/null
#thundera ononono
#thundera --help
#thundera ./testfiles/libwebrtc.a.zip
thundera ./testfiles/libLogger.a

echo "Deactivating Thundera ENV"
deactivate
echo "Deleting Thundera ENV"
rm -rf thundera_env/
