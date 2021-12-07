#!/usr/bin/env bash

### main
set -e

if [ -z "$APP_ENV" ]; then
  echo "Please set APP_ENV"
  exit 1
fi

DIRECTORY="/srv/root"
PATTERN="*.py"

# db migrations and seeding
if [[ "$APP_ENV" != "production" ]] ; then
    /scripts/migrate-db up
    /scripts/seed-db up
fi


if [ "$APP_ENV" == "local" ]; then
  EXTRA_PARAMS="watchmedo auto-restart --recursive --pattern=$PATTERN --directory=$DIRECTORY"
  SECOMND_PARAM="--"
fi

cd /srv/root

# Start services
case $APP_COMPONENT in
  "tests")
    /scripts/run_tests.sh
    ;;

  "server" | *)
     $EXTRA_PARAMS python $SECOMND_PARAM -m app.boot \
    ;;
esac
