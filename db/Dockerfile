# pull official base image
FROM postgres:15.4

RUN apt-get update \
    && apt-get -y install net-tools netcat-traditional gcc \
    && apt-get clean

# run create.sql on init
ADD create.sql /docker-entrypoint-initdb.d