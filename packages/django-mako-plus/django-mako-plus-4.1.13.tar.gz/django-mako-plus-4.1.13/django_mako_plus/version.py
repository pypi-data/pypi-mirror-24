# This file should have NO imports and be entirely standalone.
# This allows it to import into the runtime DMP as well as
# setup.py during installation.

__version__ = '4.1.13'


# Reminder on uploading to pypi and removing the build folders:
'''

python3 setup.py sdist
twine upload dist/*
rm -rf dist/ django_mako_plus.egg-info/

'''
