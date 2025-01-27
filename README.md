##ORQUESTRADOR DA ADVENTURE WORKS

Para esse projeto foi realizada a criação de um DAG com quatro etapas:
(clone_repo >> dbt_deps >> dbt_run >> dbt_test).

Ele está programado para iniciar todos os dias às 2h da manhã e executar suas tarefas em sequência.

   Tarefa 1 - clone_repo
Clonar o repositório do Projeto de dbt da AW.
 
   Tarefa 2 - dbt_deps
Ativar os pacotes necessários para os comandos utilizados nas tarefas seguintes.

   Tarefa 3 -  dbt_run 
	Rodas os modelos criados. É nessa etapa que as tabelas e visualizações são criadas no DW.

   Tarefa 4 -  dbt_test
	Roda os testes estabelecidos para os dados, para garantir que as informações estejam sendo fornecidas dentro do esperado.
