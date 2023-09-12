# This docker file will create a docker image on top of the datadog base agent
# and provision a datadog Postgres configuration file based on DB urls in env MONITOR_DATABASE_URLS
FROM datadog/agent:7

ADD entrypoint.py /entrypoint.py

RUN pip install ruamel.yaml
COPY combined_entry_point.sh /etc/cont-init.d/00-config-mysql.sh
