#!/bin/bash

# Replace PID with the actual process ID of the running Jekyll server
PID=$(pgrep -f 'jekyll serve')

if [ ! -z "$PID" ]; then
  kill -15 $PID
fi

clear

git pull origin
git merge origin/ms-dev --sign
bundle install
bundle exec jekyll build --trace
bundle exec jekyll serve --host=45.33.11.32 > /dev/null 2>&1 &

