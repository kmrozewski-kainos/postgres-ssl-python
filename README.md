# Overview
This PoC shows how to create docker with SSL-enabled postgres and connection to the database via SSL from Python 2.7 and package `psycopg2`.

# Getting started
1. Run `./start-docker.sh` to start docker with SSL-enabled docker - directory `postgres-data` is used as docker volume for postgres and it will contain generated certs and keys for both - client and server.
2. Run `./copy-keys.sh` to copy client keys needed to connect to postgres via SSL
3. In `./postgres-python` to connect to the database via SSL and run some SQL queries in the `__init__.py` python script

## Sources
### Used postgres docker with SSL from this repository
https://github.com/arc-ts/postgres-ssl
### PostgreSQL adapter for Python 2.7
http://initd.org/psycopg/