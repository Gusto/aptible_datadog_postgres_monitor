import os
from urllib.parse import urlparse
from ruamel import yaml

def get_db_instance_dict(db_url, tags):
    url_components = urlparse(db_url)
    host = url_components.hostname
    port = url_components.port
    username = url_components.username
    password = url_components.password
    database_instance = """\
 -  server: {host}
    user: {username}
    pass: '{password}'
    port: {port}
    tags: {tags}
    options:
      replication: true
      galera_cluster: true
      extra_status_metrics: true
      extra_innodb_metrics: true
      extra_performance_metrics: true
      schema_size_metrics: false
      disable_innodb_metrics: false
    """.format(host=host, username=username, password=password, port=port, tags=tags)

    return database_instance


def get_database_url_with_index(index):
    return os.environ.get('DB_URL_{}'.format(index), None)


def get_database_tags_with_index(index):
    tag_environment_key = 'DB_TAGS_{}'.format(index)
    return os.environ[tag_environment_key].split(',')


def get_database_instances():
    instances = []
    database_number = 1
    while get_database_url_with_index(database_number):
        db = get_database_url_with_index(database_number)
        tags = get_database_tags_with_index(database_number)
        instances += [get_db_instance_dict(db, tags)]
        database_number += 1
    return instances


if __name__ == "__main__":
    instances = "\n".join(get_database_instances())
    yaml_dict = """\
init_config:

instances:
{instances}
    """.format(instances=instances)

    with open('/etc/datadog-agent/conf.d/mysql.d/conf.yaml', 'w') as outfile:
        data = yaml.round_trip_load(yaml_dict, preserve_quotes=True)
        yaml.round_trip_dump(data, outfile)
