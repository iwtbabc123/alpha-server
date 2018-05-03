#!/bin/sh

echo "running process gate1......"

path=`pwd`

${path}/gate_server --gate1 1>../log/log.gate1 2>&1 &