#!/bin/bash

PYTHONPATH="." pytest -W ignore::DeprecationWarning
