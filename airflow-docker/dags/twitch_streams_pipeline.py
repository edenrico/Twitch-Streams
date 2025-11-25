from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from datetime import datetime, timedelta
import sys, os
sys.path.append('/opt/airflow')

from stages.raw.get_streams import collect_all_streams
from stages.raw.upload_s3 import s3_upload_parquet
from stages.raw.send_sqs import enviar_para_sqs
import pandas as pd

default_args = {
    "owner": "enrico",
    "retries": 1,
    "retry_delay": timedelta(minutes=3)
}

def extract_streams(**context):
    print("Iniciando coleta de dados...")
    df = collect_all_streams()
    
    if df.empty:
        print("Nenhum dado retornado da API.")
        return []

    print(f"Coletados {len(df)} registros.")
    registros = df.to_dict('records')
    context['ti'].xcom_push(key="registros", value=registros)
    return registros

def load_s3_raw(**context):
    registros = context['ti'].xcom_pull(task_ids="extract_streams", key="registros") or []
    if not registros:
        print("Sem registros para carregar no S3.")
        return
    
    df = pd.DataFrame(registros)
    print("Iniciando upload para S3 (Caminho Batch)...")
    s3_upload_parquet(df)
    print("Upload para S3 concluído.")

def publish_sqs(**context):
    registros = context['ti'].xcom_pull(task_ids="extract_streams", key="registros") or []
    if not registros:
        print("Sem registros para enviar para SQS.")
        return

    print(f"Iniciando envio de {len(registros)} eventos para SQS (Caminho Real-Time)...")
    for evento in registros:
        enviar_para_sqs(evento) 
    print("Envio para SQS concluído.")
        
with DAG(
    "twitch_streams_pipeline",
    default_args=default_args,
    description="Pipeline para capturar e salvar dados da Twitch no S3",
    schedule_interval="@hourly",
    start_date=datetime(2025, 11, 6),
    catchup=False,
) as dag:

    extract_streams_task = PythonOperator(
        task_id="extract_streams",
        python_callable=extract_streams
    )

    load_s3_raw_task = PythonOperator(
        task_id="load_s3_raw",
        python_callable=load_s3_raw
    )

    publish_sqs_task = PythonOperator(
        task_id="publish_sqs",
        python_callable=publish_sqs
    )
    
    run_silver_etl_job_task = GlueJobOperator(
        task_id="run_silver_etl_job",
        job_name="silver_glue",
        aws_conn_id="AWS_GLUE",
        run_job_kwargs={}
    )
    
    run_gold_etl_job_task = GlueJobOperator(
        task_id="run_gold_etl_job",
        job_name="gold_glue",
        aws_conn_id="AWS_GLUE",
        run_job_kwargs={}
    )
    
    extract_streams_task >> [load_s3_raw_task, publish_sqs_task] >> run_silver_etl_job_task >> run_gold_etl_job_task
