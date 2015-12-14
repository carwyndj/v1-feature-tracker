# v1-feature-tracker
track feature completion in v1

This app needs Python2.7 which you can get here; http://www.activestate.com/activepython/downloads

Installation
------------
1. Download the zip unpack code. 
2. Go to the install dir
3. Run python setup install

Usage
-----
```
v1_feature_tracker-script.py [-h] [-filename FILENAME] [-art ART] user password team [team ...]

positional arguments:
  user                V1 user name
  password            V1 password
  team                The V1 team to track the features for.

optional arguments:
  -h, --help          show this help message and exit
  -filename FILENAME  Excel file name to create (default is 'v1_features.xlsx')
  -art ART            The V1 base planning level e.g. Secure Player (ART) (default is 'Secure Player (ART)')
```
