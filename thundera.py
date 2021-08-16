#!/usr/bin/env python3
import os
from thundera import thundera


os.environ['LANG'] = 'C.UTF-8'
os.environ['LC_ALL'] = 'C.UTF-8'

thundera.cli()
