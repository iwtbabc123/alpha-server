#!/bin/sh

echo "running process db1......"

path=`pwd`

${path}/server --db1 1>../log/log.db1 2>&1 &