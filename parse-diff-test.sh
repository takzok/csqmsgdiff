#!/bin/bash

python csqmsgdiff.py scrape 800 ./test/html/800 ./test/csv/800
python csqmsgdiff.py scrape 900 ./test/html/900 ./test/csv/900
python csqmsgdiff.py scrape 910 ./test/html/910 ./test/csv/910

python csqmsgdiff.py diff ./test/csv/800 ./test/csv/900 ./test/diff/800-900 
python csqmsgdiff.py diff ./test/csv/800 ./test/csv/910 ./test/diff/800-910 
python csqmsgdiff.py diff ./test/csv/900 ./test/csv/910 ./test/diff/900-910 