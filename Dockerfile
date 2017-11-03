# This docker file will create a docker image on top of the datadog base agent
# and provision a datadog Postgres configuration file based on DB urls in env MONITOR_DATABASE_URLS
FROM datadog/docker-dd-agent
RUN apt-get update && apt-get -y install vim postgresql
ADD entrypoint.py /entrypoint.py
ADD combined_entry_point.sh /combined_entry_point.sh

ENTRYPOINT ["/combined_entry_point.sh"]
CMD ["./opt/datadog-agent/agent/agent.py", "foreground", "--profile", "--verbose"]
