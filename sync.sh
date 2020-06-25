#!/bin/bash

# Sync all domains
# docker run -ti --rm -v $PWD:/opt/data flrt/ihe-tf-sync python sync.py
# Sync ITI, RAD domains
# docker run -ti --rm -v $PWD:/opt/data flrt/ihe-tf-sync python sync.py -domain ITI,RAD

if [ $# -eq 1 ]
  then
  	echo "Sync domains : $1"
	docker run -ti --rm -v ${PWD}:/opt/data flrt/ihe-tf-sync python ihesync/sync.py --domain $1
  else
  	echo "Sync all domains"
  	docker run -ti --rm -v ${PWD}:/opt/data flrt/ihe-tf-sync python ihesync/sync.py
fi