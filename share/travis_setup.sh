#!/bin/bash
set -evx

mkdir ~/.qbiccore

# safety check
if [ ! -f ~/.qbiccore/.qbic.conf ]; then
  cp share/qbic.conf.example ~/.qbiccore/qbic.conf
fi
