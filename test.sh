#!/bin/bash

. ./venv/bin/activate
. ./env.ini

PYTHONPATH="." 

export PYTHONPATH

./venv/bin/pytest -W ignore::DeprecationWarning
