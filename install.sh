#!/bin/bash

echo "Creating virtual environment to ./env ..."
virtualenv ./env
source ./env/bin/activate
echo "Installing requirements ..."
pip install -r requirements.txt

current_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

echo "Creating wcup.sh launch script ..."

touch ./wcup.sh
echo "#!/bin/bash" >> ./wcup.sh
echo "source $current_dir/env/bin/activate" >> ./wcup.sh
echo "python $current_dir/src/main.py \$1" >> ./wcup.sh
chmod u+x ./wcup.sh

echo "Create symbolic link to /usr/local/bin/wcup ..."
echo "Enter your password to provide permission ..."

sudo ln -s $current_dir/wcup.sh /usr/local/bin/wcup
echo "Done. Thank you!"