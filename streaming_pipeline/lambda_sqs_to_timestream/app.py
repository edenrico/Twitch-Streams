import boto3
import json
import os
from decimal import Decimal # IMPORTANTE: Para converter floats (ex: duracao_min)

# --- Inicialização ---

# 1. Obter o nome da tabela do DynamoDB a partir das variáveis de ambiente
# (Configure esta variável na sua função Lambda)
DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME')

# 2. Inicializar o "recurso" do DynamoDB
dynamodb_resource = boto3.resource('dynamodb')

# 3. Validação
if not DYNAMODB_TABLE_NAME:
    raise ValueError("A variável de ambiente 'DYNAMODB_TABLE_NAME' não foi definida.")
    
# 4. Obter o objeto da tabela
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
            # 1. Obter o corpo da mensagem (que é uma string JSON)
            message_body_str = record.get('body')
            if not message_body_str:
                print(f"Mensagem {message_id} está vazia, pulando.")
                continue
            
            # 2. Converter a string JSON em um dicionário Python ('data')
            data = json.loads(message_body_str)
            
            # --- 3. MAPEAMENTO (O "DE-PARA") ---
            # Aqui nós traduzimos os nomes do seu JSON 'raw'
            # para os nomes das colunas do DynamoDB
            
            # Converte 'duracao_min' (que é float) para Decimal
            # Usa str() na conversão para evitar perda de precisão
            duracao_decimal = Decimal(str(data.get('duracao_min', 0.0)))

            item_to_put = {
                # Schema DynamoDB <-- Chave do JSON 'raw'
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
                'tags':            data.get('tags', []) # DynamoDB aceita listas
            }
            
            # 4. Validação (Garantir que as chaves obrigatórias existem)
            if not item_to_put['nome_streamer'] or not item_to_put['timestamp']:
                print(f"Erro na Mensagem {message_id}: Faltando Partition Key (streamer) ou Sort Key (inicio).")
                failed_message_ids.append(message_id)
                continue 

            # 5. Inserir o item no DynamoDB
            table.put_item(Item=item_to_put)

        except Exception as e:
            # Se algo falhar (parse, conversão Decimal, escrita no DynamoDB)
            print(f"Erro ao processar a Mensagem {message_id}: {e}")
            failed_message_ids.append(message_id)

    # --- 6. Manipulação de Falhas (Importante para SQS) ---
    if failed_message_ids:
        print(f"Falha ao processar {len(failed_message_ids)} mensagens.")
        # Lança uma exceção para o SQS saber que o lote falhou
        # O lote irá para a DLQ após N tentativas.
        raise Exception(f"Falha ao processar mensagens: {', '.join(failed_message_ids)}")

    # Se tudo correu bem
    print("Lote processado com sucesso.")
    return {
        'statusCode': 200,
        'body': json.dumps('Lote processado com sucesso.')
    }