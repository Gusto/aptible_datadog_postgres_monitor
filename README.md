[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## What is this?
- This is a small app meant to be deployed on Aptible that can monitor postgres databases.

## How do I use this in Aptible?
1. Create a new aptible app in the Aptible dashboard called `datadog_postgres_monitor`.  You should be able to put it any environment, because you can access any DB instance from ANY app and ANY environment in Aptible.  This also means you only need one app to monitor all of your DB instances.
2. Find the names of the databases you want to monitor with
```bash
aptible db:list
```
3.  Grant datadog privileges to all DBs you want to monitor by running
```
export DATADOG_USER_PASSWORD=YOUR_DATADOG_PASSWORD
aptible db:execute DATABASE_NAME grant_datadog_privileges.sql
```

Note: You will not be able to create the datadog user in replicas, because `SELECT pg_is_in_recovery() == true`.  However, you should not need to because the user will be replicated over.
3. Find the database urls of all of the postgres instances you want to monitor under 'CREDENTIALS -> Reveal' within each app database page.  You can also
5. Set environmental variables that the monitoring app needs to function.  The tags are used to uniquely identify what is being monitored.
```bash
aptible config:set --app APP_NAME --environment ENVIRONMENT_NAME \
LOG_LEVEL=DEBUG \
API_KEY=DATADOG_API_KEY \
DB_URL_1=dburl1 \
DB_URL_2=db2url \
DB_TAGS_1=aptible_env:ENVIRONMENT_NAME,aptible_app:APTIBLE_APP_NAME,env:ENVIRONMENT_NAME,app:APP_NAME,db:DATABASE_NAME \
DB_TAGS_2=aptible_env:ENVIRONMENT_NAME,aptible_app:APTIBLE_APP_NAME,env:ENVIRONMENT_NAME,app:APP_NAME,db:DATABASE_NAME
# As many DB URLs and tags as you'd like to monitor
```
7. Clone this repo and push the code to the `datadog_postgres_monitor` remote
8. You should now be able to login to datadog and view your app's DB stats for all of your database instances.

## Helpful commands:

Run the datadog agent normally
`/etc/init.d/datadog-agent start`

Run the datadog agent verbosely
`./opt/datadog-agent/agent/agent.py start --profile --verbose`

Check the datadog monitoring logs:
```bash
aptible logs --app datadog_postgres_monitor --environment ENVIRONMENT_NAME
```

Run the docker container locally
1. Set a local private IP address to be a loopback address on your host machine: `sudo ifconfig lo0 alias 192.168.46.49`
2. In `/usr/local/var/postgres/postgresql.conf` listen on all ports

```
listen_addresses = '*'
```
3. In `/usr/local/var/postgres/pg_hba.conf` add a user that can talk to locally aliased ports

```
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# My local machine IP
host    all         all         10.101.130.47/24    trust
host    all         all         192.168.46.49/24    trust
```
4. Start docker with `--net=host` and the aliased port
```bash
docker build . -t datadog_postgres_monitor
docker run -e LOG_LEVEL=DEBUG -e TAGS='postgres-monitoring-local' --net=host -e API_KEY=123 \
-e DB_URL_1=postgresql://datadog:password@192.168.46.49:5432 \
-e DB_TAGS_1=aptible_env:local_environment,aptible_app:local_app_name,env:local_environment,app:local_app_name,db:local_db \
-it DOCKER_IMAGE_ID bash
```

Note: You may have to set `ssl` to False and the db name to whatever your local database name is (type `\c` in the postgres shell to get the database name).
