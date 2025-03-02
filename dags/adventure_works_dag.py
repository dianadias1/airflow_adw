from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
     'owner': 'airflow',
     'depends_on_past': False,
     'email': ['desafioindiciumdiana@gmail.com'],
     'email_on_failure': True,
     'email_on_retry': False,
     'email_on_success': True,
     'retries': 1,
}

with DAG(
     dag_id='adventure_works_dag',
     default_args=default_args,
     description='Executa DBT em Snowflake',
     schedule_interval="0 2 * * *",
     start_date=days_ago(1),
     catchup=False,
     tags=['dbt', 'snowflake'],
) as dag:

     # Tarefa para pegar a modelagem do repositório
     clone_repo = BashOperator(
          task_id='clone_dbt_repo',
          bash_command='rm -rf /tmp/dbt-modelos && git clone https://github.com/dianadias1/adventureworks.git /tmp/dbt-modelos',
     )

     # Baixando as dependências do DBT para conseguir rodar os comando
     dbt_deps = BashOperator(
          task_id='dbt_deps',
          bash_command='export PATH="/home/airflow/.local/bin:$PATH" && cd /tmp/dbt-modelos && dbt deps',
     )

     # Rodar as transformações DBT para poder criar as tabelas lá no DW
     dbt_run = BashOperator(
          task_id='dbt_run',
          bash_command='export PATH="/home/airflow/.local/bin:$PATH" && cd /tmp/dbt-modelos && dbt run',
     )

     # Rodar os testes do DBT para ver se as taebças criadas estão dentro dos parametros definidos
     dbt_test = BashOperator(
          task_id='dbt_test',
          bash_command='export PATH="/home/airflow/.local/bin:$PATH" && cd /tmp/dbt-modelos && dbt test',
     )

     # Ordem para as tarefas acontecerem
     clone_repo >> dbt_deps >> dbt_run >> dbt_test