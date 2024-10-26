#!/bin/bash
set -e

host="$1"
shift
until curl -s "$host" > /dev/null; do
  >&2 echo "Prefect server is unavailable - sleeping"
  sleep 1
done
>&2 echo "Prefect server is up - executing command"
exec "$@"
