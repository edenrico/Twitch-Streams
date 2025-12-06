import boto3
import json
import os
from decimal import Decimal

DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME')

dynamodb_resource = boto3.resource('dynamodb')

if not DYNAMODB_TABLE_NAME:
    raise ValueError("A variável de ambiente 'DYNAMODB_TABLE_NAME' não foi definida.")
    
table = dynamodb_resource.Table(DYNAMODB_TABLE_NAME)

def lambda_handler(event, context):
    """
    Handler principal do Lambda.
    Acionado por um lote de mensagens do SQS.
    Mapeia os campos da 'raw' e os insere no DynamoDB.
    """
    
    print(f"Recebidos {len(event.get('Records', []))} registros do SQS.")
    
    failed_message_ids = []

    for record in event.get('Records', []):
        message_id = record.get('messageId')
        
        try:
            message_body_str = record.get('body')
            if not message_body_str:
                print(f"Mensagem {message_id} está vazia, pulando.")
                continue
            
            data = json.loads(message_body_str)

            duracao_decimal = Decimal(str(data.get('duracao_min', 0.0)))

            item_to_put = {
                'nome_streamer':   data.get('streamer'),    # (Partition Key)
                'timestamp':   data.get('inicio'),      # (Sort Key)
                'categoria':       data.get('categoria'),
                'idioma':          data.get('idioma'),
                'viewers':         int(data.get('viewers', 0)),
                'duracao_min':     duracao_decimal,
                'hora':            int(data.get('hora', 0)),
                'dia_semana':      data.get('dia_semana'),
                'user_id':         data.get('user_id'),
                'game_id':         data.get('game_id'),
                'is_mature':       data.get('is_mature'),
                'tags':            data.get('tags', [])
            }
            
            if not item_to_put['nome_streamer'] or not item_to_put['timestamp']:
                print(f"Erro na Mensagem {message_id}: Faltando Partition Key (streamer) ou Sort Key (inicio).")
                failed_message_ids.append(message_id)
                continue
            
            table.put_item(Item=item_to_put)

        except Exception as e:
            print(f"Erro ao processar a Mensagem {message_id}: {e}")
            failed_message_ids.append(message_id)

    if failed_message_ids:
        print(f"Falha ao processar {len(failed_message_ids)} mensagens.")
        raise Exception(f"Falha ao processar mensagens: {', '.join(failed_message_ids)}")

    print("Lote processado com sucesso.")
    return {
        'statusCode': 200,
        'body': json.dumps('Lote processado com sucesso.')
    }