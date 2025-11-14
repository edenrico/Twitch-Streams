from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from datetime import datetime, timedelta
import sys, os
sys.path.append('/opt/airflow')

from stages.raw.get_streams import collect_all_streams
from stages.raw.upload_s3 import s3_upload_parquet
from stages.raw.send_sqs import enviar_para_sqs

default_args = {
    "owner": "enrico",
    "retries": 1,
    "retry_delay": timedelta(minutes=3)
}

def extract_and_load():
    print("Iniciando coleta de dados...")
    df = collect_all_streams()
    
    if df.empty:
        print("Nenhum dado retornado da API.")
        return

    print(f"Coletados {len(df)} registros.")

    print("Iniciando upload para S3 (Caminho Batch)...")
    s3_upload_parquet(df)
    print("Upload para S3 concluído.")

    print(f"Iniciando envio de {len(df)} eventos para SQS (Caminho Real-Time)...")

    lista_de_eventos = df.to_dict('records')
    
    for evento in lista_de_eventos:
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

    extract_load_task = PythonOperator(
        task_id="extract_and_load",
        python_callable=extract_and_load
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
    
    extract_load_task >> run_silver_etl_job_task >> run_gold_etl_job_task