#!/bin/bash
/opt/datadog-agent/embedded/bin/python /entrypoint.py && /entrypoint.sh
exec "$@"
