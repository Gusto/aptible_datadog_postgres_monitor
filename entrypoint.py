import os
from urlparse import urlparse
from yaml import dump


def get_db_instance_dict(db_url, tags):
    url_components = urlparse(db_url)
    host = url_components.hostname
    port = url_components.port
    username = url_components.username
    password = url_components.password
    database_instance = {
        'host': host,
        'port': port,
        'username': username,
        'password': password,
        'dbname': 'postgres',
        'ssl': False,
        'tags': tags
    }

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
    yaml_dict = {
        'init_config': '',
        'instances': get_database_instances()
    }

    with open('/conf.d/postgres.yaml', 'w') as outfile:
        dump(yaml_dict, outfile, default_flow_style=False)
