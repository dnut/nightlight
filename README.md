Run nightlight.py and keep it running continuously. The included systemd service can manage this for you if you copy nightlight.py to /usr/local/bin/nightlight and make it executable. Running install.sh as non-root *should* take care of this for you on most linux systems.

## Dependencies
- python>=3.7
- redshift
- ddccontrol
- requests

## todo
- user config file
- gradual changes (global and per-transition)
- more times than just sunrise and sunset
- customizable hooks - not just ddccontrol and redshift
- PKGBUILD
- setup.py