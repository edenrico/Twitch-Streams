import boto3
import json
import os

name = 'SQS_QUEUE_NAME'
value = 'Twitch-real-time-sqs'

queue_name = os.getenv('SQS_QUEUE_NAME')
region_name = os.getenv('AWS_REGION')

sqs = boto3.client('sqs', region_name=region_name)

try:
    response = sqs.get_queue_url(QueueName=region_name)
    queue_url = response['QueueUrl']
except Exception as e:
    print(f"Erro CRÍTICO ao inicializar SQS: Não foi possível encontrar a fila '{queue_name}'. {e}")
    queue_url = None 

def enviar_para_sqs(dados_para_enviar):
    if not queue_url:
        print("Erro: URL da fila SQS não está definida. Mensagem não enviada.")
        return

    try:
        message_body_string = json.dumps(dados_para_enviar, default=str)
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body_string
        )
        # print(f"Mensagem enviada com sucesso! ID: {response['MessageId']}")
    except Exception as e:
        print(f"Erro ao enviar mensagem individual para o SQS: {e}")