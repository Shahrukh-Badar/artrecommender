#!/bin/sh

curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
apt-get install git-lfs
git lfs install
git lfs clone https://github.com/metmuseum/openaccess
python3 main_test.py
python3 main.py
#exec "$@"