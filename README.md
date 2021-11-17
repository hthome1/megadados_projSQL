# megadados_projSQL

Projeto SQL usando FAST API - Engenharia da computação - Insper.

## Instruções de inicialização

1. Execute o arquivo sql_app.sql - Ele que irá criar o Banco de Dados para o projeto
2. Crie um arquivo chamado '.env' com as seguintes variáveis de ambiente:
> SQL_APP_USER="seu usuario que não seja o root"
> 
> SQL_APP_PASS="sua senha do MYSQL"
3. No seu terminal dentro da raiz do repositório rode o comando:
> **$ uvicorn sql_app.main:app --reload**
