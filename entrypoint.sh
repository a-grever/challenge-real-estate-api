#!/bin/bash

set -e

timeout 90s bash -c "until pg_isready -h $DATABASE_HOST -p $DATABASE_PORT -d $DATABASE_NAME -U $DATABASE_USER ; do sleep 5 ; done"

make migration
uvicorn app.main:app --host 0.0.0.0 --port 80
