#!/bin/bash

cd build/html
zip -rq ../../docs.zip *
cd ../..

sftp docuser@omikron.pw <<< $'put docs.zip'
ssh docuser@omikron.pw <<< $'rm -rf /var/www/html/doc/centreon/*\nunzip -q -d /var/www/html/doc/centreon docs.zip\nrm docs.zip'
rm docs.zip
