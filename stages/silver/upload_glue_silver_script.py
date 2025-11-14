import boto3
import logging

s3_client = boto3.client('s3')

arquivo_local = 'silver_glue.py'   
bucket_destino = 'twitch-streams-s3' 
pasta_destino_s3 = 'scripts/'         

chave_completa_s3 = f"{pasta_destino_s3}{arquivo_local}"

try:
    s3_client.upload_file(
        arquivo_local,   
        bucket_destino,     
        chave_completa_s3  
    )
    print(f"Upload bem-sucedido: {arquivo_local} para s3://{bucket_destino}/{chave_completa_s3}")

except FileNotFoundError:
    logging.error(f"Erro: O arquivo local '{arquivo_local}' não foi encontrado.")
except Exception as e:
    logging.error(f"Erro ao fazer upload do arquivo: {e}")