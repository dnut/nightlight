Run nightlight.py and keep it running continuously. The included systemd service can manage this for you if you copy nightlight.py to /usr/local/bin/nightlight and make it executable.

## Dependencies
- python>=3.7
- redshift
- ddccontrol
- requests

## todo
- user config file
- gradual changes
- more times than just sunrise and sunset
- customizable hooks - not just ddccontrol and redshift
- PKGBUILD
- setup.py