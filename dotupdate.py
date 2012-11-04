#!/usr/bin/python
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
from dotupdate import install

def main():
    install()

if __name__ == "__main__":
    main()
