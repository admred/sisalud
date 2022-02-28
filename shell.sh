#!/bin/bash

. ./venv/bin/activate
. ./env.ini
exec python3 -mflask  shell 
