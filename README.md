# Projeto de Pipeline de Dados de Cervejarias com Airflow

Este projeto implementa um pipeline de dados utilizando o Apache Airflow para extrair dados de uma API pública de cervejarias, transformá-los e agregá-los em diferentes formatos. Além disso, o projeto inclui um sistema de alerta de falha por e-mail.

## Pré-requisitos

* **Docker:** Certifique-se de ter o Docker instalado em seu sistema. Você pode verificar a instalação com o comando:
    ```bash
    docker --version
    ```
* **Docker Compose:** O Docker Compose também é necessário para orquestrar os serviços definidos no arquivo `docker-compose.yml`. Verifique a instalação com:
    ```bash
    docker-compose --version
    ```
* **Git:** Para clonar o repositório e gerenciar versões. Você pode verificar se está instalado com:
    ```bash
    git --version
    ```

## Configuração do Ambiente

Siga os passos abaixo para configurar o ambiente utilizando o Docker Compose:

1.  **Acesse o diretório desejado:**
    ```bash
    cd <<nome_da_pasta>>
    ```
    Substitua `<<nome_da_pasta>>` pelo caminho da pasta onde você deseja clonar o projeto.

2.  **Clone o repositório do projeto:**
    ```bash
    git clone [https://github.com/pedroresd1/project-brewery-db](https://github.com/pedroresd1/project-brewery-db)
    ```

3.  **Entre no diretório do projeto:**
    ```bash
    cd project-brewery-db
    ```

4.  **Gere uma nova Secret Key para o Webserver do Airflow:**
    Execute o script Python para gerar uma chave secreta:
    ```bash
    python secret-key.py
    ```
    Copie a chave que será exibida no terminal. Exemplo: `XGOfpr2nYZR5lRUkSRM9oxmyBuj4OOoJv3AwYPK5UIw=`

5.  **Configure a Secret Key no `docker-compose.yaml`:**
    Abra o arquivo `docker-compose.yaml` com um editor de texto e localize a seção `airflow`. Dentro da seção `environment`, procure pela variável `AIRFLOW__WEBSERVER__SECRET_KEY` e substitua o valor existente pela chave que você copiou do terminal.

    ```yaml
    services:
      airflow:
        # ... outras configurações ...
        environment:
          # ... outras variáveis ...
          AIRFLOW__WEBSERVER__SECRET_KEY=XGOfpr2nYZR5lRUkSRM9oxmyBuj4OOoJv3AwYPK5UIw=
          # ... outras variáveis ...
    ```
    **Certifique-se de colar a chave correta!**

6.  **Inicie os serviços Docker:**
    Execute o seguinte comando no terminal para iniciar os containers definidos no `docker-compose.yaml`:
    ```bash
    docker-compose up -d
    ```
    Este comando irá criar e iniciar os containers do PostgreSQL, Airflow webserver e Airflow scheduler em segundo plano.

## Executando o Projeto

1.  **Acesse a interface web do Airflow:**
    Abra seu navegador e acesse o endereço:
    ```
    http://localhost:8080/login
    ```

2.  **Faça login no Airflow:**
    Utilize as seguintes credenciais padrão:
    * **Login:** `admin`
    * **Password:** `admin`

3.  **Verifique o status dos containers Docker:**
    Você pode verificar se todos os componentes do Docker estão funcionando corretamente executando o seguinte comando no terminal:
    ```bash
    docker ps
    ```
    Você deverá ver os containers `projectbrewerydb_postgres_1`, `projectbrewerydb_airflow_1` e `projectbrewerydb_airflow-scheduler_1` (ou nomes similares dependendo da configuração do seu Docker Compose) com o status "Up".

4.  **Execute a DAG:**
    Na interface web do Airflow, localize a DAG chamada `brewery_data_pipeline` e clique no botão "Play" (geralmente um ícone de ">") para iniciar a execução manual da DAG.

5.  **Monitore a execução da DAG:**
    Clique no nome da DAG (`brewery_data_pipeline`) para acessar a visão detalhada da execução. Você poderá acompanhar o status de cada task (extract\_data, transform\_data, aggregate\_data) e verificar os logs em caso de algum problema.

6.  **Verifique a criação dos arquivos:**
    Após a conclusão bem-sucedida da DAG,
