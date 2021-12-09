#!/bin/bash
scripts/build.sh
twine upload dist/* --repository thundera-bsa-test  --verbose
