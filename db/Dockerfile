FROM mysql:8.0.40-bookworm


WORKDIR /docker-entrypoint-initdb.d


COPY ./init.sql .


EXPOSE 3306
