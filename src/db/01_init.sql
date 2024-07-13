-- 01_init.sql
DROP USER IF EXISTS ns_raw_api;
CREATE USER ns_raw_api WITH SUPERUSER PASSWORD 'ns_raw_api';

DROP DATABASE IF EXISTS ns_raw_api;
CREATE DATABASE ns_raw_api WITH OWNER ns_raw_api;
