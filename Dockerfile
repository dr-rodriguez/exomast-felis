FROM postgres:16

# Some environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV ACCEPT_EULA=Y

RUN apt update && apt install -y \
    postgresql-common \
    postgresql-server-dev-all \
    libhealpix-cxx-dev \
    gnupg \
    make \
    gcc \
    g++ \
    wget \
    pkg-config

# ------------------------------------------------------------------------------------
# Postgres directory permissions
RUN chmod -R 777 /var/lib/postgresql/
RUN chmod -R 777 /var/run/postgresql/
RUN chmod -R 777 /var/run/

# ------------------------------------------------------------------------------------
# PgSphere
# https://postgrespro.github.io/pgsphere/

# Get the software
# https://github.com/postgrespro/pgsphere/archive/refs/tags/1.4.2.tar.gz
RUN wget https://github.com/postgrespro/pgsphere/archive/refs/tags/1.4.2.tar.gz
RUN tar -xzf 1.4.2.tar.gz 
WORKDIR /pgsphere-1.4.2

# Install pgsphere
# Proper installation requires HEALPIX package
RUN make PG_CONFIG=/usr/bin/pg_config USE_HEALPIX=1
RUN make install

# Clean up
RUN apt -y clean
