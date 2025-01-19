FROM apache/airflow:2.6.0

USER root

# Instalar Git
RUN apt-get update && apt-get install -y git

USER airflow

# Instalar dbt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --upgrade dbt-core dbt-snowflake

# Adicionar o diretório do dbt ao PATH
ENV PATH="/home/airflow/.local/bin:$PATH"