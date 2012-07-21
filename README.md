pacman-rdepfinder
=================

finds rdeps of a package (recursion is possible)

usage: rdepends.py [-h] [--recdepth RECDEPTH] <package name>

Recursively list all rdepends of a package.

positional arguments:
  <package name>        The name of the package.

optional arguments:
  -h, --help            show this help message and exit
  --recdepth RECDEPTH, -r RECDEPTH
                        The recursion depth (listing rdepends of rdepends)
