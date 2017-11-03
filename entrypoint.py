import os, re
from yaml import dump
from urlparse import urlparse

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
        'dbname': 'db',
        'ssl': True,
        'tags': tags
    }

    return database_instance

def get_environment_value(key):
    try:
        return os.environ[key]
    except KeyError:
        return None

def get_database_url_with_index(index):
    return get_environment_value("DB_URL_%s" % index)

def get_database_tags_with_index(index):
    return get_environment_value("DB_TAGS_%s" % index).split(',')

def get_database_instances():
    instances = []
    database_number = 1
    while get_database_url_with_index(database_number) != None:
        db = get_database_url_with_index(database_number)
        tags = get_database_tags_with_index(database_number)
        instances += [get_db_instance_dict(db, tags)]
        database_number += 1
    return instances

yaml_dict = {
    'init_config': '',
    'instances': get_database_instances()
}

with open('/conf.d/postgres.yaml', 'w') as outfile:
    dump(yaml_dict, outfile, default_flow_style=False)
