FROM mysql:8.3.0

# copy the SQL script to create the table into the container
COPY init.sql /docker-entrypoint-initdb.d/
