#!/bin/sh

SERVER_ROOT=$1
WWW_ROOT=$2

WWW_ROOT=$(echo "$WWW_ROOT" | sed 's,\\,\\\\,g' )

cd $SERVER_ROOT || exit

sed -i "s/SITE_ROOT=.*/SITE_ROOT=${WWW_ROOT}/" .env

if [ ! -d "venv" ]; then
  echo "Creating venv..."
  python -m virtualenv
fi

. ./venv/Scripts/activate
echo "Check and install python requirements"
pip install -r requirements.txt

echo "Run application"
flask --app app run