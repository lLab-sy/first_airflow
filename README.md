To initialize Airflow (macOS)

1. run `curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.2/docker-compose.yaml'` in terminal or you can check in https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
2. change `AIRFLOW__CORE__EXECUTOR: CeleryExecutor` to `AIRFLOW__CORE__EXECUTOR: LocalExecutor`
3. remove `AIRFLOW__CELERY__RESULT_BACKEND` and `AIRFLOW__CELERY__BROKER_URL`
4. remove `redis`, `airflow_worker` and `flower` defination and depend
5. save the yaml file (2-4 do in yaml file)
6. run `mkdir -p ./dags ./logs ./plugins ./config` in terminal
7. initialize database `docker compose up airflow-init` the default username and password is `airflow`
8. run airflow `docker compose up -d` and check on port 8080
9. (optional) if you don't need airflow example drag just change `AIRFLOW__CORE__LOAD_EXAMPLES: 'true'` to `AIRFLOW__CORE__LOAD_EXAMPLES: 'false'`
