#!/bin/bash
docker run -ti --rm -v $PWD:/opt/data ihe-tf-sync:1.0 python ihesync/sync.py