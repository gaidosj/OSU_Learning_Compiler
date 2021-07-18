from os import sys, path, getenv, environ
if (getenv('OLC_PROJ_DIR') is None):
    environ['OLC_PROJ_DIR'] = path.dirname(path.dirname(path.abspath(__file__)))
    sys.path.append(getenv('OLC_PROJ_DIR'))
