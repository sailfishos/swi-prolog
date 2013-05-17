#!/bin/sh
#Update library index
#this script should be in same directory with index
cd $(dirname $0)
cat INDEX-*.pl > INDEX.pl