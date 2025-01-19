from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
     'owner': 'airflow',
     'depends_on_past': False,
     'email_on_failure': False,
     'email_on_retry': False,
     'retries': 1,
}

# Configurar horários e definição da DAG
with DAG(
     dag_id='adventure_works_dag',
     default_args=default_args,
     description='Executa DBT em Snowflake',
     schedule_interval="0 2 * * *",  # Scheduled to run at 2 AM
     start_date=days_ago(1),
     catchup=False,
     tags=['dbt', 'snowflake'],
) as dag:

     # Clonar o repositório DBT
     clone_repo = BashOperator(
          task_id='clone_dbt_repo',
          bash_command='rm -rf /tmp/dbt-modelos && git clone https://github.com/dianadias1/adventureworks.git /tmp/dbt-modelos',
     )

     # Instalar dependências do DBT
     dbt_deps = BashOperator(
          task_id='dbt_deps',
          bash_command='export PATH="/home/airflow/.local/bin:$PATH" && cd /tmp/dbt-modelos && dbt deps',
     )

     # Rodar as transformações DBT
     dbt_run = BashOperator(
          task_id='dbt_run',
          bash_command='export PATH="/home/airflow/.local/bin:$PATH" && cd /tmp/dbt-modelos && dbt run',
     )

     # Rodar os testes do DBT
     dbt_test = BashOperator(
          task_id='dbt_test',
          bash_command='export PATH="/home/airflow/.local/bin:$PATH" && cd /tmp/dbt-modelos && dbt test',
     )

     # Ordem das tarefas
     clone_repo >> dbt_deps >> dbt_run >> dbt_test
