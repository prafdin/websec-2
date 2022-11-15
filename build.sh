#!/bin/bash

CLIENT_ROOT=$1

cd $CLIENT_ROOT || exit
npm install
npx vue build
