CREATE ROLE logger
  WITH LOGIN
  PASSWORD 'Pass';

CREATE DATABASE logger
  WITH OWNER = logger
       ENCODING = 'UTF8'
       TEMPLATE = template0;