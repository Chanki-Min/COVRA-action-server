#!/bin/bash

npm install
pip install --upgrade pip
pip install -r requirements.txt


mkdir -p python/data/gisaid
mkdir -p python/data/who

mkdir -p python/processed_data/gisaid
mkdir -p python/processed_data/who