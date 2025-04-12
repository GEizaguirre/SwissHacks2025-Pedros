#!/bin/bash

HOST="localhost"
USER="root"
PASSWORD="password"

docker run --name local-mysql -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 -d mysql:8

until docker exec -it local-mysql mysqladmin -h"$HOST" -u"$USER" -p"$PASSWORD" ping --silent; do
    echo "Waiting for MySQL to be ready..."
    sleep 5  # Wait 5 seconds before trying again
done

docker exec -it local-mysql mysql -uroot -ppassword -e "CREATE DATABASE \`svcr-db\`;"