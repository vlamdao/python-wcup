#!/bin/bash

echo "Creating virtual environment to ./env ..."
virtualenv ./env
source ./env/bin/activate
echo "Installing requirements ..."
pip install -r requirements.txt
echo "Create symbolic link to /usr/local/bin/wcup ..."
echo "Enter your password to provide permission ..."
chmod u+x ./wcup.sh
current_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
full_dir=$current_dir"/wcup.sh"
sudo ln -s $full_dir /usr/local/bin/wcup
echo "Done. Thank you!"
