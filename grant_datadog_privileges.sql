\set datadog_user_password `echo "$DATADOG_USER_PASSWORD"`
create user datadog with password :'datadog_user_password';
grant SELECT ON pg_stat_database to datadog;
